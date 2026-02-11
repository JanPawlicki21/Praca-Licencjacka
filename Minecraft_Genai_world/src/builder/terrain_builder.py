from typing import List, Tuple
import random
from src.domain.plan import TerrainSettings

def build_smart_terrain(width: int, length: int, settings: TerrainSettings, buildings_pos: List[Tuple[int, int]]) -> List[str]:
    """
    Generuje teren z PEŁNYMI DRZEWAMI (place feature) zamiast sadzonek.
    """
    c = []
    
    # 1. Mapa wysokości (Noise + Smoothing)
    heightmap = {}
    
    # Generowanie szumu
    for x in range(-width//2, width//2, 4):
        for z in range(-length//2, length//2, 4):
            noise = random.randint(-settings.roughness, settings.roughness)
            heightmap[(x, z)] = noise

    # Wygładzanie (Smoothing)
    for _ in range(2):
        new_map = heightmap.copy()
        for x in range(-width//2, width//2, 4):
            for z in range(-length//2, length//2, 4):
                total = 0
                count = 0
                for dx in [-4, 0, 4]:
                    for dz in [-4, 0, 4]:
                        val = heightmap.get((x+dx, z+dz))
                        if val is not None:
                            total += val
                            count += 1
                if count > 0:
                    new_map[(x, z)] = int(total / count)
        heightmap = new_map

    # Spłaszczanie pod budynki
    TARGET_OFFSET = 0 
    for (bx, bz) in buildings_pos:
        radius = 14 
        for x in range(-width//2, width//2, 4):
            for z in range(-length//2, length//2, 4):
                dist = ((x - bx)**2 + (z - bz)**2)**0.5
                if dist < radius:
                    heightmap[(x, z)] = TARGET_OFFSET
                elif dist < radius + 12:
                    factor = (dist - radius) / 12.0
                    current_h = heightmap[(x, z)]
                    heightmap[(x, z)] = int(current_h * factor + TARGET_OFFSET * (1.0 - factor))

    # 2. Generowanie bloków i DRZEW
    base_block = settings.base_block
    fill_block = "dirt"
    if base_block in ["gravel", "stone", "sand"]: fill_block = "stone"

    # Dobór typu drzewa do biomu
    tree_type = "minecraft:oak"          # Domyślnie dąb
    if "podzol" in base_block:           
        tree_type = "minecraft:jungle_tree" # Dżungla dla kawy
    elif "sand" in base_block:           
        tree_type = "minecraft:patch_cactus" # Kaktusy na piasku
    elif "spruce" in base_block or "stone" in base_block:
        tree_type = "minecraft:spruce"   # Świerki w górach

    for x in range(-width//2, width//2, 4):
        for z in range(-length//2, length//2, 4):
            offset = heightmap[(x, z)]
            
            # Wypełnienie ziemią
            c.append(f"fill ~{x} ~-30 ~{z} ~{x+3} ~{offset-1} ~{z+3} {fill_block}")
            c.append(f"fill ~{x} ~{offset} ~{z} ~{x+3} ~{offset} ~{z+3} {base_block}")
            
            # === NOWOŚĆ: SADZENIE DUŻYCH DRZEW I ROŚLINNOŚCI ===
            # Sprawdzamy czy miejsce jest wolne od budynków
            is_clear = True
            for (bx, bz) in buildings_pos:
                if ((x - bx)**2 + (z - bz)**2)**0.5 < 15: # Zwiększyłem margines do 15 kratek
                    is_clear = False
                    break
            
            if is_clear:
                # Losujemy szansę na drzewo (zależnie od vegetation z briefu)
                rng = random.randint(0, 100)
                
                # Drzewa (rzadziej, bo są duże)
                if rng < settings.vegetation * 2: 
                    # place feature stawia gotowe, duże drzewo
                    c.append(f"place feature {tree_type} ~{x+1} ~{offset+1} ~{z+1}")
                
                # Trawa i kwiatki (częściej)
                elif rng < settings.vegetation * 5:
                    decoration = "minecraft:patch_grass"
                    if rng % 2 == 0: decoration = "minecraft:flower_plain"
                    c.append(f"place feature {decoration} ~{x+1} ~{offset+1} ~{z+1}")

    return c