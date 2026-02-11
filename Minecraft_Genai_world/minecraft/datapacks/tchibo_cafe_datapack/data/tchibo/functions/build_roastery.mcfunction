fill ~ ~ ~ ~8 ~6 ~8 air
fill ~ ~-1 ~ ~8 ~-1 ~8 stone_bricks
fill ~ ~ ~ ~ ~5 ~ polished_andesite
fill ~8 ~ ~ ~8 ~5 ~ polished_andesite
fill ~ ~ ~8 ~ ~5 ~8 polished_andesite
fill ~8 ~ ~8 ~8 ~5 ~8 polished_andesite
fill ~1 ~ ~ ~7 ~4 ~ bricks
fill ~1 ~ ~8 ~7 ~4 ~8 bricks
fill ~ ~ ~1 ~ ~4 ~7 bricks
fill ~8 ~ ~1 ~8 ~4 ~7 bricks
fill ~3 ~1 ~ ~5 ~2 ~ iron_bars
fill ~3 ~1 ~8 ~5 ~2 ~8 iron_bars
fill ~ ~1 ~3 ~ ~2 ~5 iron_bars
fill ~8 ~1 ~3 ~8 ~2 ~5 iron_bars
fill ~3 ~ ~ ~5 ~1 ~ air
fill ~ ~5 ~ ~8 ~5 ~8 stone_brick_slab[type=bottom]
setblock ~6 ~5 ~6 bricks
setblock ~6 ~6 ~6 campfire
setblock ~6 ~7 ~6 brick_wall
setblock ~5 ~6 ~6 crimson_trapdoor[facing=east,open=true]
setblock ~7 ~6 ~6 crimson_trapdoor[facing=west,open=true]
setblock ~6 ~6 ~5 crimson_trapdoor[facing=south,open=true]
setblock ~6 ~6 ~7 crimson_trapdoor[facing=north,open=true]
setblock ~6 ~ ~6 blast_furnace[facing=north,lit=true]
setblock ~6 ~1 ~6 hopper
setblock ~6 ~2 ~6 iron_block
setblock ~2 ~ ~6 packed_mud
setblock ~2 ~1 ~6 packed_mud
setblock ~3 ~ ~6 packed_mud
setblock ~1 ~ ~5 barrel[facing=up]
setblock ~4 ~4 ~4 redstone_lamp
setblock ~4 ~5 ~4 lever[face=ceiling,powered=true]
setblock ~6 ~1 ~-1 spruce_wall_sign[facing=north]{front_text:{messages:['{"text":"🏭","color":"black"}','{"text":"Tchibo","bold":true,"color":"gold"}','{"text":"Roastery","color":"dark_gray"}','""']}}
tellraw @p {"text":"🏭 Coffee Roastery (Ground Level Fixed) built!","color":"gold"}
