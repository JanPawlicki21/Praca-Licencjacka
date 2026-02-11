# --- Setup Area ---
fill ~ ~ ~ ~14 ~8 ~8 air
fill ~ ~-1 ~ ~10 ~-1 ~8 dirt
# --- Main Structure ---
fill ~ ~ ~ ~10 ~ ~8 spruce_planks
fill ~ ~ ~ ~ ~4 ~ spruce_log
fill ~10 ~ ~ ~10 ~4 ~ spruce_log
fill ~ ~ ~8 ~ ~4 ~8 spruce_log
fill ~10 ~ ~8 ~10 ~4 ~8 spruce_log
fill ~ ~4 ~ ~10 ~4 ~ spruce_log
fill ~ ~4 ~8 ~10 ~4 ~8 spruce_log
fill ~ ~4 ~ ~ ~4 ~8 spruce_log
fill ~10 ~4 ~ ~10 ~4 ~8 spruce_log
fill ~1 ~1 ~1 ~9 ~3 ~1 spruce_planks
fill ~1 ~1 ~7 ~9 ~3 ~7 spruce_planks
fill ~1 ~1 ~2 ~1 ~3 ~6 spruce_planks
fill ~9 ~1 ~2 ~9 ~3 ~6 spruce_planks
# --- Windows & Doors ---
fill ~5 ~1 ~1 ~5 ~2 ~1 air
setblock ~5 ~1 ~1 oak_door[facing=south,half=lower]
setblock ~5 ~2 ~1 oak_door[facing=south,half=upper]
fill ~2 ~2 ~1 ~4 ~2 ~1 glass_pane
fill ~6 ~2 ~1 ~8 ~2 ~1 glass_pane
fill ~3 ~2 ~7 ~7 ~2 ~7 glass_pane
fill ~1 ~2 ~3 ~1 ~2 ~5 glass_pane
fill ~9 ~2 ~3 ~9 ~2 ~5 glass_pane
# --- Roof ---
fill ~-1 ~5 ~-1 ~11 ~5 ~9 spruce_slab[type=bottom]
fill ~2 ~5 ~2 ~8 ~5 ~6 spruce_slab[type=top]
# --- Tchibo Branding ---
setblock ~9 ~2 ~0 blue_wall_banner[facing=north]{BlockEntityTag:{Patterns:[{Pattern:"mr",Color:4},{Pattern:"mc",Color:4},{Pattern:"dls",Color:11},{Pattern:"bo",Color:11}]}}
setblock ~1 ~2 ~0 blue_wall_banner[facing=north]{BlockEntityTag:{Patterns:[{Pattern:"mr",Color:4},{Pattern:"mc",Color:4},{Pattern:"dls",Color:11},{Pattern:"bo",Color:11}]}}
setblock ~9 ~3 ~0 spruce_wall_sign[facing=north]{front_text:{messages:['{"text":"★","color":"gold"}','{"text":"Tchibo","bold":true,"color":"gold"}','{"text":"Kaffee & Bar","color":"white"}','""'],has_glowing_text:1b}}
setblock ~1 ~3 ~0 spruce_wall_sign[facing=north]{front_text:{messages:['{"text":"★","color":"gold"}','{"text":"Tchibo","bold":true,"color":"gold"}','{"text":"Kaffee & Bar","color":"white"}','""'],has_glowing_text:1b}}
# --- Interior ---
fill ~6 ~1 ~5 ~8 ~1 ~5 dark_oak_planks
setblock ~6 ~1 ~4 dark_oak_stairs[facing=north]
setblock ~8 ~1 ~6 water_cauldron[level=3]
setblock ~8 ~2 ~6 tripwire_hook[facing=north]
setblock ~7 ~1 ~6 barrel[facing=up]
setblock ~6 ~3 ~6 spruce_slab[type=top]
setblock ~7 ~3 ~6 blue_wall_banner[facing=north]{BlockEntityTag:{Patterns:[{Pattern:"mr",Color:4},{Pattern:"mc",Color:4},{Pattern:"dls",Color:11},{Pattern:"bo",Color:11}]}}
setblock ~8 ~3 ~6 spruce_slab[type=top]
setblock ~6 ~4 ~6 flower_pot
setblock ~2 ~1 ~2 oak_fence
setblock ~2 ~2 ~2 oak_pressure_plate
setblock ~1 ~1 ~2 oak_stairs[facing=east]
setblock ~3 ~1 ~2 oak_stairs[facing=west]
setblock ~2 ~1 ~5 oak_fence
setblock ~2 ~2 ~5 oak_pressure_plate
setblock ~3 ~1 ~5 oak_stairs[facing=west]
setblock ~5 ~4 ~3 lantern[hanging=true]
setblock ~2 ~4 ~3 lantern[hanging=true]
setblock ~8 ~4 ~3 lantern[hanging=true]
# --- Patio ---
fill ~11 ~ ~1 ~14 ~ ~5 spruce_planks
fill ~11 ~-1 ~1 ~14 ~-1 ~5 dirt
fill ~11 ~1 ~1 ~14 ~1 ~1 oak_fence
fill ~14 ~1 ~1 ~14 ~1 ~5 oak_fence
fill ~11 ~1 ~5 ~14 ~1 ~5 oak_fence
setblock ~12 ~1 ~3 oak_fence
setblock ~13 ~1 ~3 oak_stairs[facing=west]
setblock ~12 ~2 ~3 oak_fence
setblock ~12 ~3 ~3 oak_fence
setblock ~12 ~3 ~2 blue_wool
setblock ~12 ~3 ~4 blue_wool
setblock ~11 ~3 ~3 yellow_wool
setblock ~13 ~3 ~3 yellow_wool
setblock ~12 ~4 ~3 yellow_wool
# --- Finish ---
setblock ~ ~1 ~ potted_fern
setblock ~10 ~1 ~ potted_fern
tellraw @p {"text":"☕ Tchibo Cafe (Centered Banner & Fixed Sign) built!","color":"gold"}
