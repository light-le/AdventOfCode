from enum import Enum
from typing import List
from itertools import product
from pprint import pprint
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class MovingDirection(Enum):
    N = 0
    S = 1
    W = 2
    E = 3

def move_elves(extground, proposal_order):
    # first half
    elves_to_move = list()
    for r, row in enumerate(extground):
        for c, col in enumerate(row):
            if col == '#':
                to_move = check_surrounding(r, c, extground, proposal_order)
                if to_move is not None:
                    elves_to_move.append((r, c, to_move))
    # print(elves_to_move)
    if not elves_to_move:
        return 'stop round'

    # sencond half
    new_elve_positions = dict() # new_position as key, old_position as value
    for elfrow, elfcol, elfdir in elves_to_move:
        if elfdir == MovingDirection.N:
            new_position = (elfrow-1, elfcol)
        elif elfdir == MovingDirection.S:
            new_position = (elfrow+1, elfcol)
        elif elfdir == MovingDirection.W:
            new_position = (elfrow, elfcol-1)
        elif elfdir == MovingDirection.E:
            new_position = (elfrow, elfcol+1)

        if new_position in new_elve_positions:
            new_elve_positions[(elfrow, elfcol)] = None
            new_elve_positions[new_elve_positions.pop(new_position)] = None
        else:
            new_elve_positions[new_position] = (elfrow, elfcol)
            
    # print(new_elve_positions)
    for new_eposition, old_eposition in new_elve_positions.items():
        if old_eposition is not None:
            extground[old_eposition[0]][old_eposition[1]] = '.'
            extground[new_eposition[0]][new_eposition[1]] = '#'
    
    proposal_order.append(proposal_order.pop(0))

@session.submit_result(level=1, tests=[({'inp': [
    '....#..',
    '..###.#',
    '#...#.#',
    '.#...##',
    '#.###..',
    '##.#.##',
    '.#..#..'
]}, 110)])
def solve_part1(inp):
    ground = [list(line) for line in inp]
    proposal_order = list(MovingDirection.__members__.values())
    extground = ([['.' for _ in range(len(ground[0])+20)] for _ in range(10)] + 
                 [['.' for _ in range(10)] + groundl + ['.' for _ in range(10)] for groundl in ground] + 
                 [['.' for _ in range(len(ground[0])+20)] for _ in range(10)])
    
    [move_elves(extground, proposal_order) for _ in range(10)]            
    
    minrow = min([r for r, row in enumerate(extground) if '#' in row])
    maxrow = max([r for r, row in enumerate(extground) if '#' in row])
    
    mincol = min([c for c, col in enumerate([[row[c] for row in extground] for c in range(len(extground[0]))]) if '#' in col])
    maxcol = max([c for c, col in enumerate([[row[c] for row in extground] for c in range(len(extground[0]))]) if '#' in col])
    
    total_elves = sum(row.count('#') for row in extground)
    
    return (maxrow-minrow+1)*(maxcol-mincol+1) - total_elves
            

def check_surrounding(row, col, ground, proposal_order) -> MovingDirection:
    for r, c in product(range(row-1, row+2), range(col-1, col+2)):
        if r == row and c == col:
            continue
        if ground[r][c] == '#':
            return move_decision(row, col, ground, proposal_order)
    return None
        
            
def move_decision(row, col, ground, proposal_order) -> MovingDirection:
    for direction in proposal_order:
        if direction == MovingDirection.N:
            if all(ground[row-1][c] == '.' for c in range(col-1, col+2)):
                return direction
        elif direction == MovingDirection.S:
            if all(ground[row+1][c] == '.' for c in range(col-1, col+2)):
                return direction
        elif direction == MovingDirection.W:
            if all(ground[r][col-1] == '.' for r in range(row-1, row+2)):    
                return direction
        elif direction == MovingDirection.E:
            if all(ground[r][col+1] == '.' for r in range(row-1, row+2)):
                return direction

@session.submit_result(level=2, tests=[({'inp': [
    '....#..',
    '..###.#',
    '#...#.#',
    '.#...##',
    '#.###..',
    '##.#.##',
    '.#..#..'
]}, 20)])
def solve_part2(inp):
    ground = [list(line) for line in inp]
    proposal_order = list(MovingDirection.__members__.values())
    ext_spots = 1000
    extground = ([['.' for _ in range(len(ground[0])+ext_spots*2)] for _ in range(ext_spots)] + 
                 [['.' for _ in range(ext_spots)] + groundl + ['.' for _ in range(ext_spots)] for groundl in ground] + 
                 [['.' for _ in range(len(ground[0])+ext_spots*2)] for _ in range(ext_spots)])
    
    round = 0
    while True:
        round+=1
        if move_elves(extground, proposal_order) == 'stop round':
            return round


if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
