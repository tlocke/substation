import csv
import collections
import itertools
import os
import sys

tiles = []

MAX_KVA = 250

with open(os.path.join(os.getcwd(), 'input.csv')) as f:
    reader = csv.reader(f)
    next(reader)
    for x, y, kva in reader:
        tiles.append((int(x), int(y), int(kva)))
        
max_x = max(tl[0] for tl in tiles)
max_y = max(tl[1] for tl in tiles)
        
initial_map = [[None] * (max_x + 1) for i in range(max_y + 1)]
initial_map[tiles[0][1]][tiles[0][0]] = 0
prev_states = [{'map': initial_map, 'substations': collections.defaultdict(int, {0: tiles[0][2]})}]
for x, y, kva in tiles[1:]:
    sys.stdout.write('x ' + str(x) + ' y ' + str(y) + '\n')
    next_states = []
    for prev_state in prev_states:
        prev_subs = prev_state['substations']
        adj_sub_ids = set()
        prev_map = prev_state['map']
        sys.stdout.write('prev map ' + str(prev_map) + '\n')
        for x_adj, y_adj in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if x_adj < 0 or x_adj > max_x or y_adj < 0 or y_adj > max_y:
                continue
            adj_sub_id = prev_map[y_adj][x_adj]
            if adj_sub_id is not None:
                adj_sub_ids.add(adj_sub_id)
        #sys.stdout.write('adj_sub_ids ' + str(adj_sub_ids) + '\n')
        perms = [(max(sub_id for sub_id in prev_subs.keys()) + 1,)]
        for i in range(len(adj_sub_ids)):
            for perm in itertools.combinations(adj_sub_ids, i + 1):
                perms.append(perm)
        for perm in perms:
            sys.stdout.write('perm ' + str(perm) + '\n')
            next_subs = prev_subs.copy()
            perm_sum = sum(next_subs[sid] for sid in perm) + kva
            #if perm_sum > MAX_KVA:
            #    sys.stdout.write('perm_sum ' + str(perm_sum) + '\n')
            #    continue
            next_map = []
            for row in prev_map:
                next_map.append(row[:])
            next_sub_id = perm[0]   
            next_map[y][x] = next_sub_id
            next_subs[next_sub_id] = perm_sum
            for sub_id in perm[1:]:
                del next_subs[sub_id]
                for row in next_map:
                    for tile in row:
                        if tile == sub_id:
                            tile = next_sub_id
            #sys.stdout.write('about to add to next states\n')
            sys.stdout.write('new map ' + str(next_map) + '\n')
            next_states.append({'map': next_map, 'substations': next_subs})
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
                kva = row[x]
                if kva is not None:
                    writer.writerow([i, kva, x, y])

