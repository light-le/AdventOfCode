from functools import cache
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

@cache
def find_surrounding_step_pos(mapt: tuple[tuple[str]], step_pos: tuple[int, int]) -> set[tuple[int, int]]:
    next_possible_step_pos = set()
    
    current_row, current_col = step_pos
    
    if current_row > 0 and mapt[current_row-1][current_col] == '.':
        next_possible_step_pos.add((current_row-1, current_col))
    if current_row < len(mapt)-1 and mapt[current_row+1][current_col] == '.':
        next_possible_step_pos.add((current_row+1, current_col))
    if current_col > 0 and mapt[current_row][current_col-1] == '.':
        next_possible_step_pos.add((current_row, current_col-1))
    if current_col < len(mapt[0]) - 1 and mapt[current_row][current_col+1] == '.':
        next_possible_step_pos.add((current_row, current_col+1))
    return next_possible_step_pos

@cache
def find_surrounding_step_pos2(mapt: tuple[tuple[str]], step_pos: tuple[int, int]) -> set[tuple[int, int]]:
    next_possible_step_pos = set()
    
    current_row, current_col = step_pos
    
    upper_row = current_row - 1
    lower_row = current_row + 1
    left_col = current_col - 1
    right_col = current_col + 1
    
    
    
    if current_row > 0 and mapt[current_row-1][current_col] == '.':
        next_possible_step_pos.add((current_row-1, current_col))
    if current_row < len(mapt)-1 and mapt[current_row+1][current_col] == '.':
        next_possible_step_pos.add((current_row+1, current_col))
    if current_col > 0 and mapt[current_row][current_col-1] == '.':
        next_possible_step_pos.add((current_row, current_col-1))
    if current_col < len(mapt[0]) - 1 and mapt[current_row][current_col+1] == '.':
        next_possible_step_pos.add((current_row, current_col+1))
    return next_possible_step_pos 

@session.submit_result(level=1, tests=[({'mapstr': [
    '...........',
    '.....###.#.',
    '.###.##..#.',
    '..#.#...#..',
    '....#.#....',
    '.##..S####.',
    '.##..#...#.',
    '.......##..',
    '.##.#.####.',
    '.##..##.##.',
    '...........'
], 'steps': 6}, 16)])
def solve_part1(mapstr: list[str], steps: int=64):
    mapl = [list(row) for row in mapstr]
    srow, *_ = [r for r, row in enumerate(mapl) if 'S' in row]
    scol = mapl[srow].index('S')
    
    mapl[srow][scol] = '.'
    mapt = tuple([tuple(row) for row in mapl])
    
    current_step_pos = step_to_pos(steps, srow, scol, mapt)
    return current_step_pos[steps]

def step_to_pos(steps, srow, scol, mapt) -> dict:
    step_pos_dict = dict()
    current_step_pos = {(srow, scol)}
    
    for step in range(steps):
        new_steps = set()
        for step_pos in current_step_pos:
            new_steps |= find_surrounding_step_pos(mapt, step_pos)
        current_step_pos = new_steps
        step_pos_dict[step+1] = len(current_step_pos)
    return step_pos_dict

def step_to_pos2(steps, srow, scol, mapt) -> dict:
    step_pos_dict = dict()
    current_step_pos = {(srow, scol)}
    
    for step in range(steps):
        new_steps = set()
        for step_pos in current_step_pos:
            new_steps |= find_surrounding_step_pos2(mapt, step_pos)
        current_step_pos = new_steps
        step_pos_dict[step+1] = len(current_step_pos)
    return step_pos_dict

@session.submit_result(level=2, tests=[({'mapstr': [
    '...........',
    '.....###.#.',
    '.###.##..#.',
    '..#.#...#..',
    '....#.#....',
    '.##..S####.',
    '.##..#...#.',
    '.......##..',
    '.##.#.####.',
    '.##..##.##.',
    '...........'
], 'steps': 6}, 16), ({'mapstr': [
    '...........',
    '.....###.#.',
    '.###.##..#.',
    '..#.#...#..',
    '....#.#....',
    '.##..S####.',
    '.##..#...#.',
    '.......##..',
    '.##.#.####.',
    '.##..##.##.',
    '...........'
], 'steps': 100}, 6536), ({'mapstr': [
    '...........',
    '.....###.#.',
    '.###.##..#.',
    '..#.#...#..',
    '....#.#....',
    '.##..S####.',
    '.##..#...#.',
    '.......##..',
    '.##.#.####.',
    '.##..##.##.',
    '...........'
], 'steps': 5000}, 16733044)])
def solve_part2(mapstr: list[str], steps: int):
    mapl = [list(row) for row in mapstr]
    srow, *_ = [r for r, row in enumerate(mapl) if 'S' in row]
    scol = mapl[srow].index('S')
    
    mapl[srow][scol] = '.'
    mapt = tuple([tuple(row) for row in mapl])
    
    step_pos = step_to_pos(66, srow, scol, mapt)
    
    print(step_pos)


if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
