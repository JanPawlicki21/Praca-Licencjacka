import random
from typing import List
from src.domain.plan import BuildingDesign

def build_dynamic_structure(design: BuildingDesign) -> List[str]:
    """
    Generuje budynki, do których faktycznie da się wejść (Puste w środku).
    """
    c = []
    
    w, h, l = design.width, design.height, design.length
    wall = design.wall_material
    roof = design.roof_material
    floor = design.floor_material
    glass = design.window_material
    
    c.append(f"say 🏗️ Buduje: {design.wall_material} ({w}x{l})...")

    # 1. Podłoga
    c.append(f"fill ~ ~ ~ ~{w-1} ~ ~{l-1} {floor}")

    # 2. Ściany i Wnętrze (NAJWAŻNIEJSZA ZMIANA)
    # Najpierw budujemy pełny blok
    c.append(f"fill ~ ~1 ~ ~{w-1} ~{h} ~{l-1} {wall}")
    # Potem WYCINAMY środek powietrzem (zostawiając 1 kratkę ściany)
    # To gwarantuje, że w środku nie będzie ziemi ani kamienia.
    c.append(f"fill ~1 ~1 ~1 ~{w-2} ~{h} ~{l-2} air")

    # 3. Okna
    c.append(f"fill ~2 ~2 ~ ~{w-3} ~{h-2} ~ {glass}")      # Front
    c.append(f"fill ~2 ~2 ~{l-1} ~{w-3} ~{h-2} ~{l-1} {glass}") # Tył
    c.append(f"fill ~ ~2 ~2 ~ ~{h-2} ~{l-3} {glass}")      # Lewo
    c.append(f"fill ~{w-1} ~2 ~2 ~{w-1} ~{h-2} ~{l-3} {glass}") # Prawo

    # 4. Wejście (Przebijamy na wylot)
    door_x = w // 2
    # Wycinamy 2 kratki w głąb (dla pewności) i 2 w górę
    c.append(f"fill ~{door_x} ~1 ~ ~{door_x} ~2 ~1 air")
    
    # Markiza
    c.append(f"fill ~{door_x-1} ~3 ~-1 ~{door_x+1} ~3 ~-1 blue_wool")
    c.append(f"setblock ~{door_x} ~3 ~-1 yellow_wool")

    # 5. Dach
    if "flat" in design.roof_type.lower():
        c.append(f"fill ~ ~{h+1} ~ ~{w-1} ~{h+1} ~{l-1} {roof}")
    else: 
        # Piramida
        for i in range(10):
            curr_w, curr_l = w - 1 - (i*2), l - 1 - (i*2)
            if curr_w < 0 or curr_l < 0: break
            c.append(f"fill ~{i} ~{h+1+i} ~{i} ~{w-1-i} ~{h+1+i} ~{l-1-i} {roof}")

    # 6. Wnętrze (Światło i Meble)
    mid_x, mid_z = w // 2, l // 2
    c.append(f"setblock ~{mid_x} ~{h} ~{mid_z} lantern[hanging=true]")
    # Lada
    c.append(f"fill ~{mid_x-1} ~1 ~{mid_z} ~{mid_x+1} ~1 ~{mid_z} dark_oak_planks")
    c.append(f"setblock ~{mid_x} ~2 ~{mid_z} brewing_stand")

    return c