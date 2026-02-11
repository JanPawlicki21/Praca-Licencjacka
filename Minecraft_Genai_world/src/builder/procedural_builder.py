import random
from typing import List
from src.domain.plan import BuildingDesign

def build_dynamic_structure(design: BuildingDesign) -> List[str]:
    """
    Generuje ZAAWANSOWANE struktury Tchibo z brandingiem i wnętrzami.
    """
    c = []
    
    # Główne wymiary
    w, h, l = design.width, design.height, design.length
    wall = design.wall_material
    roof = design.roof_material
    floor = design.floor_material
    glass = design.window_material
    
    # ---------------------------------------------------------
    # 1. GŁÓWNA BRYŁA (Main Hall)
    # ---------------------------------------------------------
    c.append(f"say 🏗️ Buduje Tchibo Experience: {w}x{l} z {wall}...")

    # Podłoga & Ściany
    c.append(f"fill ~ ~ ~ ~{w-1} ~ ~{l-1} {floor}")
    c.append(f"fill ~ ~1 ~ ~{w-1} ~{h} ~{l-1} {wall} hollow")

    # Okna (Panoramiczne - duże przeszklenia)
    c.append(f"fill ~2 ~2 ~ ~{w-3} ~{h-2} ~ {glass}")      # Front
    c.append(f"fill ~2 ~2 ~{l-1} ~{w-3} ~{h-2} ~{l-1} {glass}") # Tył
    c.append(f"fill ~ ~2 ~2 ~ ~{h-2} ~{l-3} {glass}")      # Lewo
    c.append(f"fill ~{w-1} ~2 ~2 ~{w-1} ~{h-2} ~{l-3} {glass}") # Prawo

    # Wejście (Zawsze na środku frontu)
    door_x = w // 2
    c.append(f"fill ~{door_x} ~1 ~ ~{door_x} ~2 ~ air")
    # Markiza nad wejściem (Niebiesko-Żółta Tchibo)
    c.append(f"fill ~{door_x-1} ~3 ~-1 ~{door_x+1} ~3 ~-1 blue_wool")
    c.append(f"setblock ~{door_x} ~3 ~-1 yellow_wool")

    # Dach Główny
    c.extend(_build_roof(w, h, l, roof, design.roof_type))

    # ---------------------------------------------------------
    # 2. ROZBUDOWA: SKRZYDŁO BOCZNE (Tchibo Lounge)
    # ---------------------------------------------------------
    # Dodajemy mniejszy pokój z boku (tworzy kształt litery L)
    wing_w, wing_l = w // 2 + 1, l // 2 + 1
    
    # Decyzja: Skrzydło po prawej stronie
    c.append(f"fill ~{w-1} ~ ~2 ~{w+wing_w} ~ ~{2+wing_l} {floor}") # Podłoga
    c.append(f"fill ~{w-1} ~1 ~2 ~{w+wing_w} ~{h-1} ~{2+wing_l} {wall} hollow") # Ściany
    # Przejście
    c.append(f"fill ~{w-1} ~1 ~3 ~{w-1} ~3 ~{wing_l} air") 
    # Dach Skrzydła
    c.append(f"fill ~{w-1} ~{h} ~2 ~{w+wing_w} ~{h} ~{2+wing_l} {roof}")

    # ---------------------------------------------------------
    # 3. BRANDING & WNĘTRZA (Tchibo Atmosphere)
    # ---------------------------------------------------------
    
    # A. Banery z Logo Tchibo (Niebieskie tło, Żółte słońce/ziarno)
    banner_nbt = '{BlockEntityTag:{Patterns:[{Pattern:"moj",Color:11},{Pattern:"flo",Color:11},{Pattern:"mc",Color:11},{Pattern:"bo",Color:4}]}}'
    c.append(f"setblock ~{door_x-1} ~2 ~-1 blue_wall_banner[facing=north]{banner_nbt}")
    c.append(f"setblock ~{door_x+1} ~2 ~-1 blue_wall_banner[facing=north]{banner_nbt}")

    # B. Wyposażenie wnętrza
    # Środek: Bar Kawowy
    mid_x, mid_z = w // 2, l // 2
    c.append(f"fill ~{mid_x-1} ~1 ~{mid_z} ~{mid_x+1} ~1 ~{mid_z} dark_oak_planks") # Lada
    c.append(f"setblock ~{mid_x} ~2 ~{mid_z} brewing_stand") # Ekspres do kawy
    c.append(f"setblock ~{mid_x-1} ~2 ~{mid_z} flower_pot")  # Kubek
    c.append(f"setblock ~{mid_x+1} ~2 ~{mid_z} lantern")     # Klimat

    # Stoliki dla klientów (pod oknami)
    c.append(f"setblock ~2 ~1 ~2 oak_fence")
    c.append(f"setblock ~2 ~2 ~2 brown_carpet") # Stolik 1
    c.append(f"setblock ~{w-3} ~1 ~2 oak_fence")
    c.append(f"setblock ~{w-3} ~2 ~2 brown_carpet") # Stolik 2
    
    # Oświetlenie sufitowe
    c.append(f"setblock ~{mid_x} ~{h} ~{mid_z} lantern[hanging=true]")
    c.append(f"setblock ~{w+2} ~{h-1} ~4 lantern[hanging=true]") # W skrzydle

    return c

def _build_roof(w, h, l, material, r_type):
    """Pomocnicza funkcja do dachów"""
    c = []
    if "flat" in r_type.lower():
        c.append(f"fill ~ ~{h+1} ~ ~{w-1} ~{h+1} ~{l-1} {material}")
        c.append(f"fill ~ ~{h+2} ~ ~{w-1} ~{h+2} ~{l-1} stone_slab") # Detal
    else: 
        # Piramida
        for i in range(10):
            curr_w, curr_l = w - 1 - (i*2), l - 1 - (i*2)
            if curr_w < 0 or curr_l < 0: break
            c.append(f"fill ~{i} ~{h+1+i} ~{i} ~{w-1-i} ~{h+1+i} ~{l-1-i} {material}")
    return c