import os
import shutil
from pathlib import Path
from typing import List

# Importujemy definicję Planu (żeby odczytać projekt AI)
from src.domain.plan import WorldPlan

# Importujemy Twój nowy, dynamiczny generator
from src.builder.procedural_builder import build_dynamic_structure

def write_datapack(target_directory: Path, plan: WorldPlan) -> Path:
    """
    Tworzy datapack, generując budynki dynamicznie na podstawie projektu AI.
    """
    
    brand_name = plan.brand_name
    pack_name = "tchibo_genai"
    full_path = target_directory / pack_name
    namespace = "tchibo"

    # 1. Czyszczenie starego folderu
    if full_path.exists():
        try:
            shutil.rmtree(full_path)
        except Exception as e:
            print(f"⚠️ Nie udało się usunąć starego folderu: {e}")

    # 2. Tworzenie struktury folderów
    functions_dir = full_path / "data" / namespace / "functions"
    tags_dir = full_path / "data" / "minecraft" / "tags" / "functions"
    
    functions_dir.mkdir(parents=True, exist_ok=True)
    tags_dir.mkdir(parents=True, exist_ok=True)

    # 3. Plik pack.mcmeta
    pack_mcmeta = f"""
    {{
        "pack": {{
            "pack_format": 15,
            "description": "Tchibo GenAI - {brand_name}"
        }}
    }}
    """
    (full_path / "pack.mcmeta").write_text(pack_mcmeta, encoding="utf-8")

    # ====================================================
    # 4. MECHANIZM AUTO-STARTU (load.json)
    # ====================================================
    
    load_json = f"""
    {{
        "values": [
            "{namespace}:on_load"
        ]
    }}
    """
    (tags_dir / "load.json").write_text(load_json, encoding="utf-8")
    
    # Pusty plik on_load (zostanie wypełniony przez Orchestrator)
    (functions_dir / "on_load.mcfunction").write_text("say Loading...", encoding="utf-8")

    # ====================================================
    # 5. GENEROWANIE BUDYNKÓW (DYNAMICZNIE Z AI)
    # ====================================================
    
    print("   🔨 Budowanie struktur na podstawie projektu AI...")

    for zone in plan.zones:
        # Ustalamy nazwę pliku, jakiej oczekuje Orchestrator
        z_type = zone.zone_type.lower()
        filename = "build_unknown.mcfunction"
        
        if "cafe" in z_type:
            filename = "build_cafe.mcfunction"
        elif "origin" in z_type or "plant" in z_type:
            filename = "build_plantation.mcfunction"
        elif "process" in z_type or "roast" in z_type:
            filename = "build_roastery.mcfunction"
            
        # Generujemy komendy używając nowego buildera i designu z AI
        # (zone.design to obiekt BuildingDesign wypełniony przez Gemini)
        if zone.design:
            commands = build_dynamic_structure(zone.design)
            (functions_dir / filename).write_text("\n".join(commands), encoding="utf-8")
        else:
            print(f"⚠️ Ostrzeżenie: Strefa {zone.name} nie ma projektu (design)!")

    return full_path