from math import lcm
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

@session.submit_result(level=1, tests = [({'inp': [
    'RL',
    '',
    'AAA = (BBB, CCC)',
    'BBB = (DDD, EEE)',
    'CCC = (ZZZ, GGG)',
    'DDD = (DDD, DDD)',
    'EEE = (EEE, EEE)',
    'GGG = (GGG, GGG)',
    'ZZZ = (ZZZ, ZZZ)'
]}, 2)])
def solve_part1(inp: list[str]):
    instructions, map_dict = parse_instruction_and_map(inp)
        
    return get_minimal_steps_from_current_to_final_place(instructions, map_dict, final_places={'ZZZ'})

def get_minimal_steps_from_current_to_final_place(instructions, map_dict, final_places: set[str], current_place: str='AAA'):
    steps = 0
    while current_place not in final_places:
        dir = instructions[steps % len(instructions)]
        current_place = map_dict[current_place][dir]
        steps += 1
    return steps

def parse_instruction_and_map(inp):
    instructions, empty, *map = inp
    map_dict = {}
    
    for line in map:
        place, left_right = line.split(' = ')
        left, right = left_right.replace('(', '').replace(')', '').split(', ')
        map_dict[place] = {
            'L': left, 'R': right
        }
        
    return instructions,map_dict

@session.submit_result(level=2, tests = [({'inp': [
    'LR',
    '',
    '11A = (11B, XXX)',
    '11B = (XXX, 11Z)',
    '11Z = (11B, XXX)',
    '22A = (22B, XXX)',
    '22B = (22C, 22C)',
    '22C = (22Z, 22Z)',
    '22Z = (22B, 22B)',
    'XXX = (XXX, XXX)'
]}, 6)])
def solve_part2(inp: list[str]):
    instructions, map_dict = parse_instruction_and_map(inp)
    
    a_places = [place for place in map_dict if place.endswith('A')]
    z_places = {place for place in map_dict if place.endswith('Z')}
    
    min_steps = [get_minimal_steps_from_current_to_final_place(instructions, map_dict, z_places, current_place=cp) for cp in a_places]
    
    return lcm(*min_steps)


if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
