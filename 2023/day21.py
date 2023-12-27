from collections import namedtuple
import numpy as np
from functools import cache
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))
Point = namedtuple('Point', ['row', 'col'])

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

def find_surrounding_steps(p: Point, mapd: dict, n: int, history: set=None) -> set[Point]:
    history = history or set()
    next_steps = set()
    
    surrounding_points = [
        Point(p.row-1, p.col), # upper
        Point(p.row+1, p.col), # lower
        Point(p.row, p.col-1), # left
        Point(p.row, p.col+1), # right
    ]

    for point in surrounding_points:
        if mapd[Point(point.row % n, point.col % n)] == '.':
            next_steps.add(point)
        
    return next_steps - history
    
def derive_spots_from_steps(s: int, mat_x: np.array) -> int:
    mat_s = [s**2, s, 1]
    lix = [round(s[0]) for s in list(mat_x)]
    return sum([a*b for a,b in zip(mat_s, lix)])

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
], 'nsteps': 500}, 167004), ({'mapstr': [
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
], 'nsteps': 1000}, 668697), ({'mapstr': [
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
], 'nsteps': 5000}, 16733044)], print_only=True)
def solve_part2(mapstr: list[str], nsteps: int=26501365):
    mapl = [list(row) for row in mapstr]
    srow, *_ = [r for r, row in enumerate(mapl) if 'S' in row]
    scol = mapl[srow].index('S')
    
    mapl[srow][scol] = '.'
    mapd = dict()
    for r, row in enumerate(mapl):
        for c, char in enumerate(row):
            mapd[Point(r, c)] = char
    
    spoint = Point(srow, scol)

    history = {
        0: set(), # even steps
        1: set(), # odd steps
    }
    
    nrows = len(mapl)
    ncols = len(mapl[0])
    assert nrows == ncols
    
    outer_points = {spoint}
    
    spots_by_steps = dict()
    correct_count = 0
    
    for steps in range(1, 10*2*ncols):
        history[(steps-1)%2] |= outer_points
        new_points = set()
        for opoint in outer_points:
            next_steps = find_surrounding_steps(opoint, mapd, n=ncols, history=history[steps%2])
            new_points |= next_steps
        
        outer_points = new_points
        
        if steps >= 10*ncols:
            predicted_outers = spots_by_steps[steps-2*ncols][0] + (spots_by_steps[steps-2*ncols][0] - spots_by_steps[steps-2*2*ncols][0])
            if predicted_outers == len(outer_points):
                correct_count += 1
            else:
                correct_count = 0
        
        spots_by_steps[steps] = (len(outer_points), len(history[steps%2]), len(outer_points) + len(history[steps%2]))
        
        if correct_count >= 2*2*ncols:
            print(f'Thesis validated at steps {steps}. Breaking out')
            break
        
        if steps % 100 == 0:
            print(steps, correct_count)
    
    remainder_steps = nsteps % (2*ncols)
    final_steps = steps - (2*ncols) - (((steps - 2*ncols) % (2*ncols)) - remainder_steps)
    assert final_steps % (2*ncols) == remainder_steps
    assert final_steps <= steps
    
    # ax**2 + bx + c = s where x is steps/blocks and s is the number of spots. We're solving system of 3 
    # equations and 3 coefficients variables
    
    unknowns = list()
    total_spots = list()
    for _ in range(3):
        unknowns.append([final_steps**2, final_steps, 1])
        total_spots.append([spots_by_steps[final_steps][2]])
        
        final_steps -= (2*ncols)
    
    # arrange y = Ax where x is vector a b c 
    mat_a = np.array(unknowns)

    y = np.array(total_spots)
    print(mat_a, total_spots)

    mat_ainv = np.linalg.inv(mat_a)
    x = np.dot(mat_ainv, y)
    print('matx', x)
    test_steps = final_steps - 2*ncols
    
    for i in range(3):
        if test_steps < 2*ncols:
            break
        predicted = derive_spots_from_steps(test_steps, x)
        actual = spots_by_steps[test_steps][2]
        assert predicted == actual, \
            f'not correct at {i}th test steps {test_steps}, predited {predicted} while actual {actual}'
        test_steps -= 2*ncols

    return derive_spots_from_steps(nsteps, x)
    
if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
