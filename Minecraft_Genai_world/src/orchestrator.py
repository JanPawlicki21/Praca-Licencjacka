import os
import math
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
        
        save_path_str = os.getenv("MINECRAFT_SAVE_PATH")
        if save_path_str:
            path_obj = Path(save_path_str)
            self.target_dir = path_obj if path_obj.name == "datapacks" else path_obj / "datapacks"
            self.target_dir.mkdir(parents=True, exist_ok=True)
            print(f"📂 CEL ZAPISU: {self.target_dir}")
        else:
            self.target_dir = self.root / "generated_datapacks"

    def run_pipeline(self, brief: MarketingBrief):
        print(f"🚀 Generowanie świata TCHIBO: {brief.brand_name}")
        plan = generate_world_plan(brief)
        pack_path = write_datapack(self.target_dir, plan)
        self._create_setup_world(pack_path, plan)
        self._create_on_load_message(pack_path, plan, brief)
        print(f"✅ GOTOWE! Raport zapisany.")

    def _create_on_load_message(self, pack_path: Path, plan, brief: MarketingBrief):
        on_load_file = pack_path / "data" / "tchibo" / "functions" / "on_load.mcfunction"
        user_req = brief.user_request if hasattr(brief, 'user_request') else "Auto"
        
        cmds = []
        cmds.append('tellraw @a ["", {"text":"\\n================================\\n", "color":"dark_gray"}]')
        cmds.append('tellraw @a ["", {"text":" ☕ TCHIBO GEN-AI v5.0\\n", "color":"gold", "bold":true}]')
        cmds.append(f'tellraw @a ["", {{"text":" 🔑 Opis: ", "color":"gray"}}, {{"text":"{user_req}\\n", "color":"white"}}]')
        cmds.append(f'tellraw @a ["", {{"text":" 🏗️ Budynki: ", "color":"gray"}}, {{"text":"{len(plan.zones)} szt.", "color":"aqua", "bold":true}}]')
        
        click_cmd = "/function tchibo:setup_world"
        cmds.append(f'tellraw @a ["", {{"text":"\\n   >>> ", "color":"white"}}, {{"text":"[KLIKNIJ, ABY ZBUDOWAĆ]", "color":"green", "bold":true, "clickEvent":{{"action":"run_command", "value":"{click_cmd}"}}}}, {{"text":" <<<\\n", "color":"white"}}]')
        
        on_load_file.write_text("\n".join(cmds), encoding="utf-8")

    def _create_setup_world(self, pack_path: Path, plan):
        function_file = pack_path / "data" / "tchibo" / "functions" / "setup_world.mcfunction"
        
        cmds = []
        cmds.append('title @a title {"text":"GEN-AI BUILD","color":"gold"}')
        cmds.append('title @a subtitle {"text":"Tworzenie struktur...","color":"yellow"}')

        # 1. Teren
        cmds.extend(build_smart_terrain(160, 160, plan.terrain, [])) 

        # 2. Obliczanie pozycji (Koło)
        # Rozstawiamy budynki równomiernie na kole o promieniu 45 kratek
        num_zones = len(plan.zones)
        positions = []
        radius = 45
        
        if num_zones > 0:
            angle_step = 360 / num_zones
            for i in range(num_zones):
                angle_rad = math.radians(i * angle_step)
                x = int(radius * math.cos(angle_rad))
                z = int(radius * math.sin(angle_rad))
                positions.append((x, z))
        
        # 3. Ścieżki (Dla KAŻDEJ wyliczonej pozycji)
        path_mat = plan.terrain.path_material
        cmds.append(f"say 🛣️ Łączenie {num_zones} budynków ścieżkami z {path_mat}...")
        
        for pos in positions:
            # Droga od (0,0) do budynku
            cmds.extend(build_connection_path(0, 0, pos[0], pos[1], path_mat))

        # 4. Centrum
        cmds.append("fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 stone_bricks")
        cmds.append("setblock ~ ~1 ~ beacon")

        # 5. Budynki
        for i, zone in enumerate(plan.zones):
            x, z = positions[i] # Bierzemy wyliczoną pozycję
            
            # Ustalanie nazwy pliku (zgodnie z mcfunction_builder)
            z_type = zone.zone_type.lower()
            func_name = "build_unknown"
            if "cafe" in z_type: func_name = "build_cafe"
            elif "origin" in z_type or "plant" in z_type: func_name = "build_plantation"
            elif "process" in z_type or "roast" in z_type: func_name = "build_roastery"
            
            cmds.append(f"execute positioned ~{x} ~1 ~{z} run function tchibo:{func_name}")
            
            # Tabliczka
            sign_text = f'[\'{{\"text\":\"{zone.name}\",\"color\":\"blue\",\"bold\":true}}\']'
            cmds.append(f"setblock ~{x} ~2 ~{z-6} oak_sign[rotation=8]{{front_text:{{messages:{sign_text}}}}}")

        cmds.append('title @a title {"text":"GOTOWE!","color":"green"}')
        cmds.append("playsound entity.player.levelup master @a ~ ~ ~ 1 1")

        function_file.write_text("\n".join(cmds), encoding="utf-8")