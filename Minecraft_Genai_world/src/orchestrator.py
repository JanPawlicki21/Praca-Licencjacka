import os
import json
from pathlib import Path
from dotenv import load_dotenv

from src.domain.brief import MarketingBrief
from src.genai.plan_generator import generate_world_plan
from src.builder.mcfunction_builder import write_datapack
from src.builder.terrain_builder import build_smart_terrain 
from src.builder.path_builder import build_connection_path

class Orchestrator:
    def __init__(self, project_root: Path):
        self.root = project_root
        load_dotenv(dotenv_path=project_root / '.env')
        
        # Logika ścieżki
        save_path_str = os.getenv("MINECRAFT_SAVE_PATH")
        if save_path_str:
            path_obj = Path(save_path_str)
            if path_obj.name == "datapacks":
                self.target_dir = path_obj
            else:
                self.target_dir = path_obj / "datapacks"
            self.target_dir.mkdir(parents=True, exist_ok=True)
            print(f"📂 CEL ZAPISU: {self.target_dir}")
        else:
            self.target_dir = self.root / "generated_datapacks"

    def run_pipeline(self, brief: MarketingBrief):
        print(f"🚀 Generowanie świata TCHIBO: {brief.brand_name}")
        
        # 1. AI generuje plan
        plan = generate_world_plan(brief)
        
        # 2. Tworzenie Datapacka (folderów i load.json)
        pack_path = write_datapack(self.target_dir, plan)
        
        # 3. Wypełnienie raportu (on_load) i funkcji budującej (setup_world)
        self._create_on_load_message(pack_path, plan, brief)
        self._create_setup_world(pack_path, plan)
        
        print(f"✅ GOTOWE! Raport zapisany. Wpisz /reload w grze.")

    def _create_on_load_message(self, pack_path: Path, plan, brief: MarketingBrief):
        """
        Wypełnia plik on_load.mcfunction, który gra uruchomi AUTOMATYCZNIE po reloadzie.
        """
        on_load_file = pack_path / "data" / "tchibo" / "functions" / "on_load.mcfunction"
        
        keywords_str = ", ".join(brief.keywords)
        biom_info = f"{plan.terrain.base_block.upper().replace('_', ' ')}"
        
        cmds = []
        # Puste linie dla czytelności
        cmds.append('tellraw @a ["", {"text":"\\n\\n================================\\n", "color":"dark_gray"}]')
        
        # Nagłówek
        cmds.append('tellraw @a ["", {"text":" ☕ TCHIBO GEN-AI ", "color":"gold", "bold":true}, {"text":"v3.0\\n", "color":"yellow"}]')
        
        # Dane z AI
        cmds.append(f'tellraw @a ["", {{"text":" 🔑 Prompt: ", "color":"gray"}}, {{"text":"{keywords_str}\\n", "color":"white"}}]')
        cmds.append(f'tellraw @a ["", {{"text":" 🌍 AI Biom: ", "color":"gray"}}, {{"text":"{biom_info}", "color":"aqua", "bold":true}}, {{"text":" (Roślinność: {plan.terrain.vegetation})\\n", "color":"gray"}}]')
        
        # KLIKALNY PRZYCISK [GENERUJ]
        click_cmd = "/function tchibo:setup_world"
        cmds.append(f'tellraw @a ["", {{"text":"\\n   >>> ", "color":"white"}}, {{"text":"[KLIKNIJ, ABY ZBUDOWAĆ]", "color":"green", "bold":true, "clickEvent":{{"action":"run_command", "value":"{click_cmd}"}}, "hoverEvent":{{"action":"show_text", "value":"Generuj teren i budynki"}}}}, {{"text":" <<<\\n", "color":"white"}}]')
        
        cmds.append('tellraw @a ["", {"text":"================================\\n", "color":"dark_gray"}]')
        
        # Dźwięk "Pling"
        cmds.append("playsound block.note_block.pling master @a ~ ~ ~ 1 2")

        on_load_file.write_text("\n".join(cmds), encoding="utf-8")

    def _create_setup_world(self, pack_path: Path, plan):
        function_file = pack_path / "data" / "tchibo" / "functions" / "setup_world.mcfunction"
        
        cmds = []
        cmds.append('title @a title {"text":"GEN-AI MAGIC","color":"gold"}')
        cmds.append('title @a subtitle {"text":"Materializacja wizji...","color":"light_purple"}')

        # 1. Generowanie Terenu (Podłoga biomu)
        # Rozszerzamy teren, żeby ścieżki się zmieściły
        cmds.extend(build_smart_terrain(160, 160, plan.terrain, [])) 

        # 2. Definicja Pozycji Budynków
        # Hub (Środek)
        hub_pos = (0, 0)
        
        # Pozycje stref (naokoło Huba)
        positions = [
            (0, 45),   # Północ
            (-45, 0),  # Zachód
            (45, 0)    # Wschód
        ]

        # 3. Budowanie Ścieżek (NAJPIERW drogi, potem budynki)
        path_mat = plan.terrain.path_material
        cmds.append(f"say 🛣️ Wylewam drogi z {path_mat}...")
        
        for pos in positions:
            # Łączymy (0,0) z (x, z)
            cmds.extend(build_connection_path(0, 0, pos[0], pos[1], path_mat))

        # 4. Centrum (Rynek / Hub)
        cmds.append("fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 stone_bricks") # Placyk centralny
        cmds.append("setblock ~ ~1 ~ beacon") # Beacon na środku!

        # 5. Budowanie Budynków w ustalonych miejscach
        for i, zone in enumerate(plan.zones):
            # Dobieramy pozycję z listy (lub domyślną, jeśli zabraknie)
            if i < len(positions):
                x, z = positions[i]
            else:
                x, z = (0, 60 + (i*10))

            z_type = zone.zone_type.lower()
            func_name = "build_unknown"
            
            # Mapowanie nazw plików (musi się zgadzać z mcfunction_builder)
            if "cafe" in z_type: func_name = "build_cafe"
            elif "origin" in z_type or "plant" in z_type: func_name = "build_plantation"
            elif "process" in z_type or "roast" in z_type: func_name = "build_roastery"
            
            # Wywołanie funkcji budującej w konkretnym miejscu
            # rotacja (ostatni param) jest uproszczona
            cmds.append(f"execute positioned ~{x} ~1 ~{z} run function tchibo:{func_name}")
            
            # Tabliczka informacyjna przed budynkiem
            # Ustawiamy ją przy ścieżce
            sign_text = f'[\'{{\"text\":\"{zone.name}\",\"color\":\"blue\",\"bold\":true}}\']'
            cmds.append(f"setblock ~{x} ~2 ~{z-6} oak_sign[rotation=8]{{front_text:{{messages:{sign_text}}}}}")

        cmds.append('title @a title {"text":"GOTOWE!","color":"green"}')
        cmds.append("playsound entity.player.levelup master @a ~ ~ ~ 1 1")

        function_file.write_text("\n".join(cmds), encoding="utf-8")