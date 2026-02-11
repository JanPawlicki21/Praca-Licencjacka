from __future__ import annotations
from typing import List

def build_cafe_mcfunction() -> List[str]:
    """
    Generuje strefę 'Home Cafe' (Kawiarnia Tchibo).
    Wersja zaawansowana z patio, meblami i brandingiem.
    """
    c: List[str] = []

    # --- Setup Area ---
    c.append("fill ~ ~ ~ ~14 ~8 ~8 air")
    c.append("fill ~ ~-1 ~ ~10 ~-1 ~8 dirt")

    # --- Main Structure ---
    c.append("fill ~ ~ ~ ~10 ~ ~8 spruce_planks")
    # Filary
    c.append("fill ~ ~ ~ ~ ~4 ~ spruce_log")
    c.append("fill ~10 ~ ~ ~10 ~4 ~ spruce_log")
    c.append("fill ~ ~ ~8 ~ ~4 ~8 spruce_log")
    c.append("fill ~10 ~ ~8 ~10 ~4 ~8 spruce_log")
    # Belki poziome
    c.append("fill ~ ~4 ~ ~10 ~4 ~ spruce_log")
    c.append("fill ~ ~4 ~8 ~10 ~4 ~8 spruce_log")
    c.append("fill ~ ~4 ~ ~ ~4 ~8 spruce_log")
    c.append("fill ~10 ~4 ~ ~10 ~4 ~8 spruce_log")
    # Ściany
    c.append("fill ~1 ~1 ~1 ~9 ~3 ~1 spruce_planks")
    c.append("fill ~1 ~1 ~7 ~9 ~3 ~7 spruce_planks")
    c.append("fill ~1 ~1 ~2 ~1 ~3 ~6 spruce_planks")
    c.append("fill ~9 ~1 ~2 ~9 ~3 ~6 spruce_planks")

    # --- Windows & Doors ---
    c.append("fill ~5 ~1 ~1 ~5 ~2 ~1 air")
    c.append("setblock ~5 ~1 ~1 oak_door[facing=south,half=lower]")
    c.append("setblock ~5 ~2 ~1 oak_door[facing=south,half=upper]")
    # Szyby
    c.append("fill ~2 ~2 ~1 ~4 ~2 ~1 glass_pane")
    c.append("fill ~6 ~2 ~1 ~8 ~2 ~1 glass_pane")
    c.append("fill ~3 ~2 ~7 ~7 ~2 ~7 glass_pane")
    c.append("fill ~1 ~2 ~3 ~1 ~2 ~5 glass_pane")
    c.append("fill ~9 ~2 ~3 ~9 ~2 ~5 glass_pane")

    # --- Roof ---
    c.append("fill ~-1 ~5 ~-1 ~11 ~5 ~9 spruce_slab[type=bottom]")
    c.append("fill ~2 ~5 ~2 ~8 ~5 ~6 spruce_slab[type=top]")

    # --- Tchibo Branding ---
    # Używamy potrójnego cudzysłowu, żeby nie psuć JSON-a w środku
    banner_nbt = '{BlockEntityTag:{Patterns:[{Pattern:"mr",Color:4},{Pattern:"mc",Color:4},{Pattern:"dls",Color:11},{Pattern:"bo",Color:11}]}}'
    c.append(f"setblock ~9 ~2 ~0 blue_wall_banner[facing=north]{banner_nbt}")
    c.append(f"setblock ~1 ~2 ~0 blue_wall_banner[facing=north]{banner_nbt}")
    
    sign_json = "['{\"text\":\"★\",\"color\":\"gold\"}','{\"text\":\"Tchibo\",\"bold\":true,\"color\":\"gold\"}','{\"text\":\"Kaffee & Bar\",\"color\":\"white\"}','\"\"']"
    c.append(f"setblock ~9 ~3 ~0 spruce_wall_sign[facing=north]{{front_text:{{messages:{sign_json},has_glowing_text:1b}}}}")
    c.append(f"setblock ~1 ~3 ~0 spruce_wall_sign[facing=north]{{front_text:{{messages:{sign_json},has_glowing_text:1b}}}}")

    # --- Interior ---
    c.append("fill ~6 ~1 ~5 ~8 ~1 ~5 dark_oak_planks")
    c.append("setblock ~6 ~1 ~4 dark_oak_stairs[facing=north]")
    c.append("setblock ~8 ~1 ~6 water_cauldron[level=3]")
    c.append("setblock ~8 ~2 ~6 tripwire_hook[facing=north]")
    c.append("setblock ~7 ~1 ~6 barrel[facing=up]")
    c.append("setblock ~6 ~3 ~6 spruce_slab[type=top]")
    c.append(f"setblock ~7 ~3 ~6 blue_wall_banner[facing=north]{banner_nbt}")
    c.append("setblock ~8 ~3 ~6 spruce_slab[type=top]")
    c.append("setblock ~6 ~4 ~6 flower_pot")
    
    # Stoliki
    c.append("setblock ~2 ~1 ~2 oak_fence")
    c.append("setblock ~2 ~2 ~2 oak_pressure_plate")
    c.append("setblock ~1 ~1 ~2 oak_stairs[facing=east]")
    c.append("setblock ~3 ~1 ~2 oak_stairs[facing=west]")
    
    c.append("setblock ~2 ~1 ~5 oak_fence")
    c.append("setblock ~2 ~2 ~5 oak_pressure_plate")
    c.append("setblock ~3 ~1 ~5 oak_stairs[facing=west]")
    
    # Oświetlenie
    c.append("setblock ~5 ~4 ~3 lantern[hanging=true]")
    c.append("setblock ~2 ~4 ~3 lantern[hanging=true]")
    c.append("setblock ~8 ~4 ~3 lantern[hanging=true]")

    # --- Patio ---
    c.append("fill ~11 ~ ~1 ~14 ~ ~5 spruce_planks")
    c.append("fill ~11 ~-1 ~1 ~14 ~-1 ~5 dirt")
    c.append("fill ~11 ~1 ~1 ~14 ~1 ~1 oak_fence")
    c.append("fill ~14 ~1 ~1 ~14 ~1 ~5 oak_fence")
    c.append("fill ~11 ~1 ~5 ~14 ~1 ~5 oak_fence")
    c.append("setblock ~12 ~1 ~3 oak_fence")
    c.append("setblock ~13 ~1 ~3 oak_stairs[facing=west]")
    c.append("setblock ~12 ~2 ~3 oak_fence")
    c.append("setblock ~12 ~3 ~3 oak_fence")
    # Parasol
    c.append("setblock ~12 ~3 ~2 blue_wool")
    c.append("setblock ~12 ~3 ~4 blue_wool")
    c.append("setblock ~11 ~3 ~3 yellow_wool")
    c.append("setblock ~13 ~3 ~3 yellow_wool")
    c.append("setblock ~12 ~4 ~3 yellow_wool")

    # --- Finish ---
    c.append("setblock ~ ~1 ~ potted_fern")
    c.append("setblock ~10 ~1 ~ potted_fern")
    c.append('tellraw @p {"text":"☕ Tchibo Cafe (Full Version) built!","color":"gold"}')

    return c