import csv
import os
import sys
import copy

tiles = []
tile_set = set()

MAX_KVA = 250

with open(os.path.join(os.getcwd(), 'input.csv')) as f:
    reader = csv.reader(f)
    next(reader)
    for str_x, str_y, str_kva in reader:
        x = int(str_x)
        y = int(str_y)
        tiles.append((x, y, int(str_kva)))
        tile_set.add((x, y))
        
max_x = max(tl[0] for tl in tiles)
max_y = max(tl[1] for tl in tiles)

def add_tile(state, x, y, kva, sub_id):
    subs = state['substations']
    if sub_id not in subs:
        subs[sub_id] = {'sum-kva': 0, 'islands': []}
        
    sub = subs[sub_id]
    sub['sum-kva'] += kva
    islands = sub['islands']
        
    if sub['sum-kva'] > MAX_KVA:
        return False
    
    state_map = state['map']
    new_island = True
    boundary_tiles = set()
    # find boundary tiles
    for x_adj, y_adj in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
        if x_adj < 0 or x_adj > max_x or y_adj < 0 or y_adj > max_y or (x_adj, y_adj) not in tile_set:
            continue
             
        adj_sub_id = state_map[y_adj][x_adj]
        if adj_sub_id is None:
            boundary_tiles.add((x_adj, y_adj))
        elif adj_sub_id == sub_id:
            new_island = False
            
    if new_island:
        islands.append(boundary_tiles)
    else:
        join_islands = [i for i in range(len(islands)) if (x, y) in islands[i]]
        first_island = islands[join_islands[0]]
        for i in join_islands[1:]:
            first_island = first_island.union(islands[i])
        islands[join_islands[0]] = first_island.union(boundary_tiles)
        for i in join_islands[1:]:
            del islands[i]
            
    #remove any boundary tiles
    #sys.stdout.write('sub ' + str(subs) + '\n')
    for sub in subs.values():
        for island in sub['islands']:
            if (x, y) in island:
                island.remove((x, y))
    
    for sub in subs.values():
        islands = sub['islands']
        if len(islands) > 1:
            for island in islands:
                if len(island) == 0:
                    return False
                
    state_map[y][x] = sub_id
    #sys.stdout.write('map ' + str(state_map) + '\n')
    return True

prev_states = [{'map': [[None] * (max_x + 1) for i in range(max_y + 1)], 'substations': {}}]
add_tile(prev_states[0], tiles[0][0], tiles[0][1], tiles[0][1], 0)

for x, y, kva in tiles[1:]:
    sys.stdout.write('x ' + str(x) + ' y ' + str(y) + '\n')
    next_states = []
    for prev_state in prev_states:
        prev_subs_keys = list(prev_state['substations'].keys())
        for next_sub_id in [max(prev_subs_keys) + 1] + prev_subs_keys:
            next_state = copy.deepcopy(prev_state)
            if add_tile(next_state, x, y, kva, next_sub_id): 
                #sys.stdout.write('new map ' + str(next_map) + '\n')
                next_states.append(next_state)
    #sys.stdout.write('next states ' + str(next_states) + '\n')
    prev_states = next_states

with open(os.path.join(os.getcwd(), 'output.csv'), 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['solution-id', 'substation-id', 'x', 'y'])
    for i in range(len(prev_states)):
        state = prev_states[i]
        sub_map = state['map']
        for y in range(len(sub_map)):
            row = sub_map[y]
            for x in range(len(row)):
                sub_id = row[x]
                if sub_id is not None:
                    writer.writerow([i, sub_id, x, y])