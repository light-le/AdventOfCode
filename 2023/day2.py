
from utils import AdventSession, extract_year_day_from_path
from functools import reduce

session = AdventSession(**extract_year_day_from_path(__file__))

@session.submit_result(level=1, tests=[({'inp': [
    'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
    'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
    'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
    'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
    'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'
]}, 8)])
def solve_part1(inp: list[str]):
    all_cubes = {
        'red': 12,
        'green': 13,
        'blue': 14
    }
    possible_id_sum = 0
    for id, game_info in enumerate(inp, start=1):
        game_id, info = game_info.split(': ')
        cube_sets = info.split('; ')
        for cube_set in cube_sets:
            cube_counts = cube_set.split(', ')
            impossible = False # assume it's still possible
            for cube_count in cube_counts:
                cubec, cube_col = cube_count.split(' ')
                if int(cubec) > all_cubes[cube_col]:
                    impossible = True
                    break
            if impossible:
                break
        if not impossible:
            possible_id_sum += id
    return possible_id_sum
                
@session.submit_result(level=2, tests=[({'inp': [
    'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
    'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
    'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
    'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
    'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'
]}, 2286)])
def solve_part2(inp: list[str]):
    sum_of_power = 0
    for id, game_info in enumerate(inp, start=1):
        game_id, info = game_info.split(': ')
        minimum_cubes = {
            'red': 0,
            'green': 0,
            'blue': 0
        }
        cube_sets = info.split('; ')
        for cube_set in cube_sets:
            cube_counts = cube_set.split(', ')
            for cube_count in cube_counts:
                cubec, cube_col = cube_count.split(' ')
                minimum_cubes[cube_col] = max(minimum_cubes[cube_col], int(cubec))
        game_power = reduce(lambda a, b: a*b, minimum_cubes.values())
        sum_of_power += game_power
    return sum_of_power


if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
