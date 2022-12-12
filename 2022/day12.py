
from string import ascii_lowercase
from collections import namedtuple, deque
from typing import List, Tuple
from utils import AdventSession, extract_year_day_from_path

Position = namedtuple('Position', ['r', 'c'])
session = AdventSession(**extract_year_day_from_path(__file__))

class Map:
    def __init__(self, map: List, part1: bool=True) -> None:
        self.map = map
        self.part1 = part1
        
    def find(self, char: str = 'a') -> List[Position]:
        poses = list()
        for r, row in enumerate(self.map):
            if char in row:
                poses.extend([Position(r, c) for c, ch in enumerate(row) if ch == char])
        return poses
        
    def get_starting_position(self) -> Tuple[int, int]:
        for r, row in enumerate(self.map):
            if 'S' in row:
                return Position(r, row.index('S'))
            
    def get_elevation(self, pos: Position) -> int:
        s = self.map[pos.r][pos.c]
        if s == 'S':
            return 0
        elif s == 'E':
            return 25
        else:
            return ascii_lowercase.index(s)
            
    def get_available_pos(self, pos, part1: bool=True):
        possible_pos = set()
        if pos.r > 0:
            possible_pos.add(Position(pos.r-1, pos.c))
        if pos.r < len(self.map) - 1:
            possible_pos.add(Position(pos.r+1, pos.c))
        if pos.c > 0:
            possible_pos.add(Position(pos.r, pos.c-1))
        if pos.c < len(self.map[0])-1:
            possible_pos.add(Position(pos.r, pos.c+1))
        if self.part1:
            return {
                next_pos for next_pos in possible_pos if self.get_elevation(next_pos) <= (self.get_elevation(pos) + 1)
            }
        else:
            return {
                next_pos for next_pos in possible_pos if self.get_elevation(next_pos) >= (self.get_elevation(pos) - 1)
            }
    
    def is_(self, char: str, pos) -> bool:
        return self.map[pos.r][pos.c] == char
    
    def solve(self, starting_pos, ending_char: str='E') -> int:
        frontier = deque([(pos, 1) for pos in self.get_available_pos(starting_pos)])
        visited_pos = {starting_pos} | self.get_available_pos(starting_pos)
        while frontier:
            pos, step = frontier.popleft()
            if self.is_(ending_char, pos):
                return step
            available_pos = self.get_available_pos(pos)
            new_available_pos = available_pos - (available_pos & visited_pos)
            visited_pos |= new_available_pos
            frontier.extend([(pos, step+1) for pos in new_available_pos])
        raise Exception(f'Should have found {ending_char}')
    
@session.submit_result(level=1, tests=[({'inp': [
    'Sabqponm',
    'abcryxxl',
    'accszExk',
    'acctuvwj',
    'abdefghi'
]}, 31)])
def solve_part1(inp):
    spots = [list(row) for row in inp]
    map = Map(spots)
    
    starting_pos = map.get_starting_position()
    
    return map.solve(starting_pos)

@session.submit_result(level=2, tests=[({'inp': [
    'Sabqponm',
    'abcryxxl',
    'accszExk',
    'acctuvwj',
    'abdefghi'
]}, 29)])
def solve_part2(inp):
    spots = [list(row) for row in inp]
    map = Map(spots, part1=False)
    
    [e_spot] = map.find('E')
    
    return map.solve(e_spot, 'a')

if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
