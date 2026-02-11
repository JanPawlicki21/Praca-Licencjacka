from __future__ import annotations
from typing import List

def build_coffee_roastery_mcfunction() -> List[str]:
    """
    Generuje strefę 'Processing' (Palarnia Kawy).
    POPRAWKA: Obniżenie wszystkiego o 1 blok (poziom 0), aby nie lewitowało.
    """
    c: List[str] = []

    # 1. Przygotowanie terenu
    c.append("fill ~ ~ ~ ~8 ~6 ~8 air")
    c.append("fill ~ ~-1 ~ ~8 ~-1 ~8 stone_bricks") # Podłoga na poziomie -1

    # 2. Budynek
    # Filary (zostają od 0, bo były dobrze)
    c.append("fill ~ ~ ~ ~ ~5 ~ polished_andesite")
    c.append("fill ~8 ~ ~ ~8 ~5 ~ polished_andesite")
    c.append("fill ~ ~ ~8 ~ ~5 ~8 polished_andesite")
    c.append("fill ~8 ~ ~8 ~8 ~5 ~8 polished_andesite")
    
    # Ściany z cegły (POPRAWKA: start od ~, czyli 0)
    c.append("fill ~1 ~ ~ ~7 ~4 ~ bricks")          # Front
    c.append("fill ~1 ~ ~8 ~7 ~4 ~8 bricks")        # Tył
    c.append("fill ~ ~ ~1 ~ ~4 ~7 bricks")          # Lewa
    c.append("fill ~8 ~ ~1 ~8 ~4 ~7 bricks")        # Prawa
    
    # Okna (POPRAWKA: obniżone do poziomu 1-2)
    c.append("fill ~3 ~1 ~ ~5 ~2 ~ iron_bars")
    c.append("fill ~3 ~1 ~8 ~5 ~2 ~8 iron_bars")
    c.append("fill ~ ~1 ~3 ~ ~2 ~5 iron_bars")
    c.append("fill ~8 ~1 ~3 ~8 ~2 ~5 iron_bars")

    # Wejście (POPRAWKA: wycięcie od poziomu 0)
    c.append("fill ~3 ~ ~ ~5 ~1 ~ air") 

    # 3. Dach (bez zmian, na poziomie 5)
    c.append("fill ~ ~5 ~ ~8 ~5 ~8 stone_brick_slab[type=bottom]")
    
    # Komin
    c.append("setblock ~6 ~5 ~6 bricks")
    c.append("setblock ~6 ~6 ~6 campfire") 
    c.append("setblock ~6 ~7 ~6 brick_wall")
    c.append("setblock ~5 ~6 ~6 crimson_trapdoor[facing=east,open=true]") 
    c.append("setblock ~7 ~6 ~6 crimson_trapdoor[facing=west,open=true]")
    c.append("setblock ~6 ~6 ~5 crimson_trapdoor[facing=south,open=true]")
    c.append("setblock ~6 ~6 ~7 crimson_trapdoor[facing=north,open=true]")

    # 4. Maszyna do palenia kawy (POPRAWKA: stoi na poziomie 0)
    c.append("setblock ~6 ~ ~6 blast_furnace[facing=north,lit=true]")
    c.append("setblock ~6 ~1 ~6 hopper") 
    c.append("setblock ~6 ~2 ~6 iron_block") 

    # 5. Magazyn (POPRAWKA: stoi na poziomie 0)
    c.append("setblock ~2 ~ ~6 packed_mud")      # Dolny worek
    c.append("setblock ~2 ~1 ~6 packed_mud")     # Górny worek
    c.append("setblock ~3 ~ ~6 packed_mud")      # Dolny worek obok
    c.append("setblock ~1 ~ ~5 barrel[facing=up]") # Beczka

    # 6. Oświetlenie
    c.append("setblock ~4 ~4 ~4 redstone_lamp")
    c.append("setblock ~4 ~5 ~4 lever[face=ceiling,powered=true]")

    # 7. Tabliczka (POPRAWKA: obniżona do poziomu 1, wisi przed ścianą)
    sign_nbt = '''{front_text:{messages:['{"text":"🏭","color":"black"}','{"text":"Tchibo","bold":true,"color":"gold"}','{"text":"Roastery","color":"dark_gray"}','""']}}'''
    
    # Ponieważ ściana teraz wypełnia poziom 0-4, za tabliczką na pewno jest cegła.
    c.append(f"setblock ~6 ~1 ~-1 spruce_wall_sign[facing=north]{sign_nbt}")

    c.append('tellraw @p {"text":"🏭 Coffee Roastery (Ground Level Fixed) built!","color":"gold"}')
    return c