from extract_prom_data import read_map_list
import json
import shutil
from pathlib import Path

# some sheets have been cut in two pieces so there is new indexing
tileset_translate = {0:0, 1:1, 2:2, 3:3, 4:[4,5],
	5:[6,7], 6:8, 7:[9,10], 8:[11,12], 9:13, 10:14,
	11:15, 12:16, 13:17}
# where each old sheet was cut, in terms of tile indexing
cut_lengths = {"4": 4270, "5": 3920, "7": 5894, "8": 4774}

TILE_KEYS = ["Ground", "Mask", "Mask2", "Mask3", "Fringe", "Fringe2",
	"Fringe3"]
ANIM_KEYS = ["GroundAnim", "MaskAnim", "Mask2Anim", "Mask3Anim",
	"FringeAnim", "Fringe2Anim", "Fringe3Anim"]
TILE_SET_KEYS = ["GroundTileset", "MaskTileset", "Mask2Tileset",
	"Mask3Tileset", "FringeTileset", "Fringe2Tileset", "Fringe3Tileset"]
ANIM_SET_KEYS = ["GroundAnimTileset", "MaskAnimTileset", "Mask2AnimTileset",
	"Mask3AnimTileset", "FringeAnimTileset", "Fringe2AnimTileset",
	"Fringe3AnimTileset"]

# May give an offset to tile_index depending on which part it belongs to
def index_offset(tileset_index, tile_index):
	tileset_cutoff = cut_lengths[str(tileset_index)]
	if int(tile_index/tileset_cutoff) >= 1:
		part_index = 1
		tile_index = tile_index - tileset_cutoff
	else: part_index = 0
	return tile_index, part_index

def get_tile_sheet_indices(tile, tileset_index, tile_index):
    sheet_index = tileset_translate[tileset_index]
    if isinstance(sheet_index,(list)):
        tile_index, part = index_offset(tileset_index, tile_index)
        sheet_index = sheet_index[part]
    return tile_index, sheet_index

def copy_tile(tile, anim_sheet, anim_key):
    anim_index = int(tile[anim_key])
    anim_index, anim_sheet = get_tile_sheet_indices(tile, anim_sheet, anim_index)
    anim_path = Path('SheetTiles/'+str(anim_sheet)+'/'+str(anim_index+1)+'.png')
    target_path = Path('AnimTiles/'+str(anim_sheet)+'/'+str(anim_index+1)+'.png')
    shutil.copy(anim_path, target_path)

def copy_tiles(tiles):
    for tile in tiles:
        if tile['MapID'] == 's1622':
            for key_index, anim_key in enumerate(ANIM_KEYS):
                if tile[anim_key] != "0":
                    anim_sheet = int(tile[ANIM_SET_KEYS[key_index]])
                    copy_tile(tile, anim_sheet, anim_key)
                    tile_sheet = int(tile[TILE_SET_KEYS[key_index]])
                    copy_tile(tile, tile_sheet, TILE_KEYS[key_index])

def extract_tiles(map):
    with open('prom_data.json', 'r') as o2:
        tiles = json.load(o2)
        copy_tiles(tiles)

def extract_animation_tiles(map_list):
    print(map_list)
    print('Copying tiles ...')
    for map in map_list:
        extract_tiles(map)
    print('Copying complete!')

def importer():
    map_list = read_map_list()
    extract_animation_tiles(map_list)

if __name__ == "__main__":
    importer()
