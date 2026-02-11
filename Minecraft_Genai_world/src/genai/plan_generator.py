import os
import json
import re
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

from src.domain.brief import MarketingBrief
from src.domain.plan import WorldPlan, Zone, TerrainSettings, BuildingDesign

current_file = Path(__file__).resolve()
project_root = current_file.parents[2]
load_dotenv(dotenv_path=project_root / '.env')
api_key = os.getenv("GOOGLE_API_KEY")

if api_key and api_key != "OFFLINE":
    genai.configure(api_key=api_key)

def generate_world_plan(brief: MarketingBrief) -> WorldPlan:
    print(f"🧠 (AI) Analiza życzenia: '{brief.user_request}'")

    # Fallback
    default_design = BuildingDesign(
        wall_material="oak_planks", roof_material="oak_stairs", 
        floor_material="stone", window_material="glass_pane", 
        height=6, width=9, length=9, roof_type="A-frame"
    )
    fallback_plan = WorldPlan(
        brand_name=brief.brand_name,
        brand_story="Fallback",
        terrain={
            "theme": "Default", "roughness": 5, "vegetation": 5, 
            "base_block": "grass_block", "path_material": "gravel"
        },
        zones=[
            Zone(zone_type="home_cafe", name="Cafe", purpose="Social", design=default_design),
            Zone(zone_type="coffee_origin", name="Farm", purpose="Origin", design=default_design),
            Zone(zone_type="processing", name="Factory", purpose="Work", design=default_design)
        ]
    )

    if not api_key: return fallback_plan

    models = ["models/gemini-2.5-flash"]

    # --- ZMIENIONY PROMPT: DYNAMICZNA LICZBA BUDYNKÓW ---
    prompt = f"""
    Jesteś Architektem Minecraft.
    Marka: "{brief.brand_name}".
    Życzenie Gracza: "{brief.user_request}".
    
    ZADANIE:
    1. Dobierz biom (base_block) i materiał ścieżek (path_material).
    2. Zaprojektuj listę budynków (Zones).
       - Jeśli gracz nie podał liczby: zrób standardowe 3 (Kawiarnia, Plantacja, Palarnia).
       - Jeśli gracz chce "duże miasto" lub "4 budynki": wygeneruj tyle, ile chce (max 6).
    
    WYMAGANY FORMAT JSON:
    {{
      "brand_name": "{brief.brand_name}",
      "brand_story": "Opis...",
      "terrain": {{
        "theme": "Nazwa biomu", "roughness": 5, "vegetation": 5,
        "base_block": "snow_block", "path_material": "packed_ice"
      }},
      "zones": [
        {{
          "zone_type": "unique_id_1",
          "name": "Nazwa Budynku 1",
          "purpose": "Cel",
          "design": {{
             "wall_material": "snow_block", "roof_material": "blue_wool",
             "floor_material": "spruce_planks", "window_material": "ice",
             "height": 6, "width": 10, "length": 10, "roof_type": "flat"
          }}
        }},
        {{ ... (kolejne budynki - tyle ile potrzeba) ... }}
      ]
    }}
    """

    for model_name in models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            
            if match:
                data = json.loads(match.group(0))
                if "terrain" not in data: continue
                print(f"✅ AI wygenerowało {len(data.get('zones', []))} stref! (Model: {model_name})")
                return WorldPlan(**data)

        except Exception as e:
            print(f"⚠️ Błąd {model_name}: {e}")
            continue 

    return fallback_plan