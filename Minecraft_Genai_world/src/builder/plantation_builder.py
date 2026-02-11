from __future__ import annotations
from typing import List

def build_coffee_plantation_mcfunction() -> List[str]:
    """
    Generuje strefę 'Coffee Origin' (Plantacja).
    Używa flowering_azalea_leaves jako krzaków kawy.
    """
    c: List[str] = []
    
    # 1. Przygotowanie terenu
    c.append("fill ~ ~ ~ ~10 ~ ~10 podzol")
    c.append("fill ~ ~1 ~ ~10 ~5 ~10 air")

    # 2. Rzędy 'krzewów kawy'
    # Rząd 1
    c.append("fill ~2 ~1 ~2 ~2 ~1 ~8 oak_log")
    c.append("fill ~2 ~2 ~2 ~2 ~2 ~8 flowering_azalea_leaves")
    
    # Rząd 2
    c.append("fill ~5 ~1 ~2 ~5 ~1 ~8 oak_log")
    c.append("fill ~5 ~2 ~2 ~5 ~2 ~8 flowering_azalea_leaves")

    # Rząd 3
    c.append("fill ~8 ~1 ~2 ~8 ~1 ~8 oak_log")
    c.append("fill ~8 ~2 ~2 ~8 ~2 ~8 flowering_azalea_leaves")

    # 3. Drzewo cienia (Jungle Tree)
    c.append("setblock ~9 ~1 ~9 jungle_sapling")
    c.append("fill ~9 ~1 ~9 ~9 ~4 ~9 jungle_log")
    c.append("fill ~7 ~4 ~7 ~11 ~4 ~11 jungle_leaves")
    c.append("fill ~8 ~5 ~8 ~10 ~5 ~10 jungle_leaves")

    # 4. Detale (kosze i worki)
    c.append("setblock ~1 ~1 ~1 composter[level=4]")
    c.append("setblock ~3 ~1 ~5 composter[level=8]")
    c.append("setblock ~6 ~1 ~9 hay_block[axis=y]")
    c.append("setblock ~7 ~1 ~9 hay_block[axis=y]")

    # 5. Oświetlenie
    c.append("setblock ~4 ~1 ~4 oak_fence")
    c.append("setblock ~4 ~2 ~4 lantern")

    c.append('tellraw @p {"text":"🌿 Coffee Plantation (Origin Zone) built!","color":"green"}')
    return c