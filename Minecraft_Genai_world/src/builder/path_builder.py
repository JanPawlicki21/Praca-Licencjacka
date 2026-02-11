from typing import List

def build_connection_path(x1, z1, x2, z2, material="gravel") -> List[str]:
    """
    Tworzy drogę o szerokości 3 bloków łączącą punkt A (x1, z1) z punktem B (x2, z2).
    """
    cmds = []
    
    # Ustalamy wysokość drogi (lekko wkopana w ziemię lub na poziomie 0)
    y = "~-1" 
    
    # 1. Odcinek wzdłuż osi X
    # Idziemy od x1 do x2, trzymając z1 stałe
    start_x, end_x = min(x1, x2), max(x1, x2)
    
    # fill x y z x y z block
    # Robimy szerokość 3 (z-1 do z+1)
    cmds.append(f"fill {start_x} {y} {z1-1} {end_x} {y} {z1+1} {material}")
    
    # 2. Odcinek wzdłuż osi Z
    # Idziemy od z1 do z2, trzymając x2 (już osiągnięte) stałe
    start_z, end_z = min(z1, z2), max(z1, z2)
    
    cmds.append(f"fill {x2-1} {y} {start_z} {x2+1} {y} {end_z} {material}")
    
    # 3. Latarnie wzdłuż drogi (co 10 kratek)
    # To dodaje klimatu i zapobiega spawnowaniu potworów
    dist_x = abs(x2 - x1)
    if dist_x > 10:
        step = 1 if x2 > x1 else -1
        for bx in range(x1, x2, step * 10):
            cmds.append(f"setblock {bx} ~ {z1+2} oak_fence")
            cmds.append(f"setblock {bx} ~1 {z1+2} lantern")

    return cmds