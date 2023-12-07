
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

def source_to_dest(num: int, mapping: dict, source: str='seed', final_dest: str='location') -> int:
    while source != final_dest and mapping:
        source_map = mapping.pop(source)
        for key, value in source_map.items():
            if key == 'destination':
                continue
            
            source_start, source_end = key
            if source_start <= num <= source_end:
                num = value + (num - source_start)
                break
        source = source_map['destination']
        
        
        
    assert source == final_dest, f'Could not find {final_dest} in mapping dictionary'
    return num

def source_range_to_dest(range: tuple[int, int], mapping: dict, source: str='seed', final_dest: str='location') -> int:
    ranges = [range]
    while source != final_dest and mapping:
        source_map = mapping.pop(source)
        new_ranges = []
        print(ranges)
        while ranges:
            range_start, range_end = ranges.pop()
            for key, value in source_map.items():
                if key == 'destination':
                    continue
                broken = False
                
                source_map_start, source_map_end = key
                if source_map_start <= range_start <= source_map_end:
                    range_start = (range_start - source_map_start) + value
                    if range_end <= source_map_end:
                        range_end = (range_end - source_map_start) + value
                        new_ranges.append((range_start, range_end))
                        broken = True
                        break
                    else:
                        new_ranges.append((source_map_end+1, range_end))
                        range_start = source_map_end+1
                        # range_end = (source_map_end - source_map_start) + value
                        # new_ranges.append((range_start, range_end))
                elif source_map_start <= range_end <= source_map_end:
                    # new_ranges.append((range_start, source_map_start-1))
                    range_end = (range_end - source_map_start) + value
                    new_ranges.append((value, range_end))
                    range_end = source_map_start-1
                elif range_start < source_map_start < source_map_end < range_end:
                    ranges.append((source_map_end+1, range_end))
                    range_end = source_map_start-1
                    # new_ranges.append((range_start, source_map_start-1))
                    # new_ranges.append((source_map_end+1, range_end))
                    # range_start = value
                    # range_end = value + (source_map_end - source_map_start)
                    new_ranges.append((value, value + (source_map_end-source_map_start)))
                # else:
                #     new_ranges.append((range_start, range_end))
                
                if not broken:
                    new_ranges.append((range_start, range_end))
                if len(new_ranges) < 20:
                    print(new_ranges)
        print('source', source, 'source map', source_map)
        print('new ranges', new_ranges)
        ranges = new_ranges.copy()
        source = source_map['destination']
    return min([start for start, end in ranges])
            

@session.submit_result(level=1, tests=[({'inp': [
    'seeds: 79 14 55 13',
    '',
    'seed-to-soil map:',
    '50 98 2',
    '52 50 48',
    '',
    'soil-to-fertilizer map:',
    '0 15 37',
    '37 52 2',
    '39 0 15',
    '',
    'fertilizer-to-water map:',
    '49 53 8',
    '0 11 42',
    '42 0 7',
    '57 7 4',
    '',
    'water-to-light map:',
    '88 18 7',
    '18 25 70',
    '',
    'light-to-temperature map:',
    '45 77 23',
    '81 45 19',
    '68 64 13',
    '',
    'temperature-to-humidity map:',
    '0 69 1',
    '1 0 69',
    '',
    'humidity-to-location map:',
    '60 56 37',
    '56 93 4'
]}, 35)])
def solve_part1(inp: list[str]):
    mappings, seed_ints = build_mapping_seeds(inp)
    
    locations = [source_to_dest(seed_int, mappings.copy()) for seed_int in seed_ints]
    return min(locations)

def build_mapping_seeds(inp):
    l = 0
    mappings = dict()
    while l < len(inp):
        line = inp[l]
        if l == 0:
            seed, seed_nums = line.split(": ")
            seed_ints = [int(s) for s in seed_nums.split()]
            l+=1
        elif line == '':
            l+=1
        else:
            source, to, dest = line.replace(' map:', '').split('-')
            source_mapping = {'destination': dest}
            
            l+=1
            line = inp[l]
            while l < len(inp) and inp[l] != '':
                line = inp[l]
                dest_start, src_start, rale = [int(s) for s in line.split()]
                source_mapping.update({(src_start, src_start + rale - 1): dest_start})
                l+=1
            mappings[source] = source_mapping
    return mappings, seed_ints

def build_mapping_seeds2(inp: list[str]):
    seed_line, empty, *other_lines = inp
    
    seed_text, seed_values = seed_line.split(': ')
    seeds = [int(s) for s in seed_values.split()]
    
    seed_start = [seeds[i] for i in range(0, len(seeds), 2)]
    seed_range_length = [seeds[i] for i in range(1, len(seeds)+1,2)]
    
    seed_maps = sorted([(seed_start[i], seed_start[i]+seed_range_length[i]-1) for i in range(len(seed_start))], key=lambda x: x[0])
    
    mapping = {}
    for line in other_lines:
        if line == '':
            mapping[dest] = dest_mapping
        elif line[0].isdigit():
            dest_start, source_start, range_length = [int(s) for s in line.split()]
            dest_mapping['map'][(dest_start, dest_start+range_length-1)] = (source_start, source_start+range_length-1)
        else:
            source, to, dest = line.replace(' map:', '').split('-')
            dest_mapping = {'source': source, 'map': {}}
    
    mapping[dest] = dest_mapping
    return seed_maps, mapping


@session.submit_result(level=2, tests=[({'inp': [
    'seeds: 79 14 55 13',
    '',
    'seed-to-soil map:',
    '50 98 2',
    '52 50 48',
    '',
    'soil-to-fertilizer map:',
    '0 15 37',
    '37 52 2',
    '39 0 15',
    '',
    'fertilizer-to-water map:',
    '49 53 8',
    '0 11 42',
    '42 0 7',
    '57 7 4',
    '',
    'water-to-light map:',
    '88 18 7',
    '18 25 70',
    '',
    'light-to-temperature map:',
    '45 77 23',
    '81 45 19',
    '68 64 13',
    '',
    'temperature-to-humidity map:',
    '0 69 1',
    '1 0 69',
    '',
    'humidity-to-location map:',
    '60 56 37',
    '56 93 4'
]}, 46)])
def solve_part2(inp: list[str]):
    seed_ranges, mapping = build_mapping_seeds2(inp)
    
    location_ranges = sorted(mapping['location']['map'].keys(), key=lambda x: -x[0])
    min_loc = location_ranges[-1][0]
    max_loc = location_ranges[0][1]
    
    location_all_ranges = [(max_loc, float('inf'))] + location_ranges
    
    if min_loc > 0:
        location_all_ranges.append((0, min_loc-1))
    
    smallest_location = None
    while smallest_location is None:
        smallest_loc_start, smallest_loc_end = location_all_ranges.pop()
        
        current_entity = mapping['location']['source']
        ent_start = None
        ent_end = None
        for (loc_start, loc_end), (hum_start, hum_end) in mapping['location']['map'].items():
            if loc_start <= smallest_loc_start <= smallest_loc_end <= loc_end:
                ent_start = hum_start + (smallest_loc_start - loc_start)
                ent_end = ent_start + (smallest_loc_end - smallest_loc_start)
                
        if ent_start is None and ent_end is None:
            ent_start = smallest_loc_start
            ent_end = smallest_loc_end
            
        while current_entity != 'seed':
            current_map = mapping[current_entity]['map']
            # for (dest_start, dest_end), (source_start, source_end) in current_map.items():
            for dest_start, dest_end in sorted(current_map.keys(), key=lambda x: x[0]):
                source_start, source_end = current_map[(dest_start, dest_end)]
                if dest_start <= ent_start <= dest_end:
                    if ent_end <= dest_end:
                        diff = ent_end - ent_start
                        ent_start = source_start + (ent_start - dest_start)
                        ent_end = ent_start + diff
                    else:
                        ent_start = source_start + (ent_start - dest_start) # do NOT refactor this because we need diff from above 1st
                        ent_end = source_end
                        new_smallest_loc_end = smallest_loc_start + (ent_end - ent_start)
                        location_all_ranges.append((new_smallest_loc_end+1, smallest_loc_end))
                        smallest_loc_end = new_smallest_loc_end
                    break
                elif dest_start <= ent_end and ent_start <= dest_end: # for this to work it requires the for sequence to be sorted
                    # keep ent_start
                    ent_end = dest_start - 1
                    new_smallest_loc_end = smallest_loc_start + (ent_end - ent_start)
                    location_all_ranges.append((new_smallest_loc_end+1, smallest_loc_end))
                    smallest_loc_end = new_smallest_loc_end
                    break

            current_entity = mapping[current_entity]['source']
        for seed_start, seed_end in seed_ranges:
            if seed_start <= ent_start <= seed_end:
                smallest_location = smallest_loc_start
                break
            elif seed_start <= ent_end and ent_start <= seed_end:
                smallest_location = smallest_loc_start + (seed_start - ent_start)
                break
            
    return smallest_location
        

if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
