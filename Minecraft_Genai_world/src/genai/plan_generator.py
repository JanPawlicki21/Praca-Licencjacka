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

    # --- FALLBACK (Plan Awaryjny) ---
    default_design = BuildingDesign(
        wall_material="oak_planks", roof_material="oak_stairs", 
        floor_material="stone", window_material="glass_pane", 
        height=6, width=9, length=9, roof_type="A-frame"
    )
    
    # TUTAJ BYŁ BŁĄD. Zmieniamy obiekt TerrainSettings na zwykły słownik.
    # To naprawia błąd "ValidationError".
    fallback_plan = WorldPlan(
        brand_name=brief.brand_name,
        brand_story="Fallback",
        terrain={
            "theme": "Default", 
            "roughness": 5, 
            "vegetation": 5, 
            "base_block": "grass_block",
            "path_material": "gravel"  # <--- Upewnij się, że to pole jest w plan.py!
        },
        zones=[
            Zone(zone_type="home_cafe", name="Cafe", purpose="Social", design=default_design),
            Zone(zone_type="coffee_origin", name="Farm", purpose="Origin", design=default_design),
            Zone(zone_type="processing", name="Factory", purpose="Work", design=default_design)
        ]
    )

    if not api_key: return fallback_plan

    # Używamy modelu 2.0 Flash dla stabilności JSON
    models = ["models/gemini-2.5-flash"]

    prompt = f"""
    Jesteś Architektem Minecraft (Java 1.20).
    Marka: "{brief.brand_name}".
    Opis gracza: "{brief.user_request}".
    
    ZADANIE:
    1. Zinterpretuj opis i dobierz biom (base_block) oraz materiał ścieżek (path_material).
    2. Zaprojektuj 3 budynki (Kawiarnia, Plantacja, Palarnia).
    
    WYMAGANY FORMAT JSON:
    {{
      "brand_name": "{brief.brand_name}",
      "brand_story": "Opis...",
      "terrain": {{
        "theme": "Nazwa biomu",
        "roughness": 5,
        "vegetation": 5,
        "base_block": "snow_block",
        "path_material": "packed_ice"
      }},
      "zones": [
        {{
          "zone_type": "home_cafe",
          "name": "Nazwa",
          "purpose": "Cel",
          "design": {{
             "wall_material": "snow_block",
             "roof_material": "blue_wool",
             "floor_material": "spruce_planks",
             "window_material": "ice",
             "height": 6, "width": 10, "length": 10, "roof_type": "flat"
          }}
        }},
        ... (kolejne dwie strefy w tym samym formacie) ...
      ]
    }}
    """

    for model_name in models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            raw_text = response.text
            
            # Chirurgiczne wycinanie JSON
            match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            
            if match:
                clean_json = match.group(0)
                data = json.loads(clean_json)
                
                if "terrain" not in data:
                     print(f"⚠️ Model {model_name} pominął teren.")
                     continue

                print(f"✅ AI wygenerowało poprawny JSON! (Model: {model_name})")
                return WorldPlan(**data)
            else:
                print(f"⚠️ Błąd parsowania: Nie znaleziono JSON.")

        except Exception as e:
            print(f"⚠️ Błąd {model_name}: {e}")
            continue 

    print("❌ Wszystkie modele zawiodły. Uruchamiam Fallback.")
    return fallback_plan