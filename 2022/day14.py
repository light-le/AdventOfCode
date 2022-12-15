
from utils import AdventSession, extract_year_day_from_path
from collections import namedtuple
from functools import reduce
from abc import ABC
from typing import List, Set, Dict

Position = namedtuple('Position', ['x', 'y'])
session = AdventSession(**extract_year_day_from_path(__file__))

class Dust(ABC):
    def __init__(self, position: Position) -> None:
        self.position = position
    def __hash__(self) -> int:
        return hash((self.position.x, self.position.y))
    def __eq__(self, __o: object) -> bool:
        return self.__hash__() == __o.__hash__()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} {self.position}'
    
        
class Rock(Dust):
    pass

class Sand(Dust):
    def available_fallen_spot(self, dusts: Set[Dust]):
        dust_positions = {dust.position for dust in dusts}
        
        down = Position(self.position.x, self.position.y+1)
        if down not in dust_positions:
            return down
        
        down_left = Position(self.position.x-1, self.position.y+1)
        if down_left not in dust_positions:
            return down_left
        
        down_right = Position(self.position.x+1, self.position.y+1)
        if down_right not in dust_positions:
            return down_right

        return None
    
    def available_fallen_spot2(self, dusts: Dict) -> Position:
        y_below = self.position.y + 1
        
        for x in [self.position.x, self.position.x-1, self.position.x+1]:
            if x not in dusts[y_below]:
                return Position(x, y_below)
        return None
        
def parse_rock_line(txt: str) -> Set[Rock]:
    rock_pos = txt.split(' -> ')
    rocks = set()
    for rock_end1, rock_end2 in zip(rock_pos[:-1], rock_pos[1:]):
        rock_end1x, rock_end1y = [int(s) for s in rock_end1.split(',')]
        rock_end2x, rock_end2y = [int(s) for s in rock_end2.split(',')]
        
        if rock_end1x == rock_end2x:
            rocks |= {Rock(Position(rock_end1x, rocky))
                      for rocky in range(min(rock_end1y, rock_end2y),
                                         max(rock_end1y, rock_end2y)+1)}
        elif rock_end2y == rock_end1y:
            rocks |= {Rock(Position(rockx, rock_end1y))
                      for rockx in range(min(rock_end1x, rock_end2x),
                                         max(rock_end1x, rock_end2x)+1)}
    return rocks

@session.submit_result(level=1, tests=[({'inp': [
    '498,4 -> 498,6 -> 496,6',
    '503,4 -> 502,4 -> 502,9 -> 494,9'
]}, 24)])
def solve_part1(inp):
    rocks = reduce((lambda l1, l2: l1|l2), [parse_rock_line(line) for line in inp])
    
    bottom_rock_y = max([rock.position.y for rock in rocks])
    
    active_sand = None
    resting_sands = set()
    
    while True:
        if active_sand is None:
            active_sand = Sand(Position(500, 0))
        
        if active_sand.available_fallen_spot(rocks | resting_sands):
            active_sand.position = active_sand.available_fallen_spot(rocks | resting_sands)
            if active_sand.position.y > bottom_rock_y:
                return len(resting_sands)
        else:
            resting_sands.add(active_sand)
            active_sand = None

@session.submit_result(level=2, tests=[({'inp': [
    '498,4 -> 498,6 -> 496,6',
    '503,4 -> 502,4 -> 502,9 -> 494,9'
]}, 93)])
def solve_part2(inp):
    rocks = reduce((lambda l1, l2: l1|l2), [parse_rock_line(line) for line in inp])
    
    
    bottom_rock_y = max([rock.position.y for rock in rocks])
    
    max_y = bottom_rock_y + 1
    
    dusts_xy = {y: set() for y in range(max_y+1)}
    
    for rock in rocks:
        dusts_xy[rock.position.y].add(rock.position.x)
    
    active_sand = None
    
    resting_sand_count = 0
    while True:
        if active_sand is None:
            active_sand = Sand(Position(500, 0))
            resting_sand_count += 1
            
        if active_sand.position.y == max_y:
            dusts_xy[max_y].add(active_sand.position.x)
            active_sand = None
        else:
            afs = active_sand.available_fallen_spot2(dusts_xy)
            if afs:
                active_sand.position = afs
            else:
                dusts_xy[active_sand.position.y].add(active_sand.position.x)
                if active_sand.position == Position(500, 0):
                    return resting_sand_count
                active_sand = None
                


if __name__ == '__main__':
    inp = session.read_input().split('\n')
    
    solve_part1(inp)
    
    solve_part2(inp)
