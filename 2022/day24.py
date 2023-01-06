from enum import Enum
from typing import List, Set, Tuple
from itertools import cycle
from collections import defaultdict, deque, namedtuple
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class Direction(Enum):
    LEFT = '<'
    RIGHT = '>'
    UP = '^'
    DOWN = 'v'

class Entity:
    all_entities = defaultdict(set)
    def __init__(self, r: int, c: int) -> None:
        self.row = r
        self.col = c
        self.all_entities[self.__class__].add(self)
        
    def __repr__(self) -> str:
        return f'{self.row} {self.col}'
        
    def __hash__(self) -> int:
        return hash((self.row, self.col))
    
    def __eq__(self, __o: object) -> bool:
        return self.row == __o.row and self.col == __o.col

class Wind(Entity):
    def __init__(self, r, c, direction: Direction) -> None:
        super().__init__(r, c)
        self.direction = direction
       
class Wall(Entity):
    pass

class You(Entity):
    def search_near_open_spaces(self, winds: Set, walls: Set) -> List[Tuple[int, int]]:
        next_spaces = [(self.row-1, self.col), (self.row, self.col), (self.row+1, self.col),
                       (self.row, self.col-1), (self.row, self.col+1)]
        next_valid_spaces = [(row, col) for row, col in next_spaces if row >= 0 and col >= 0 and row <= 26]
        wallwinds = winds | walls
        
        return [next_space for next_space in next_valid_spaces if next_space not in wallwinds]
            
State = namedtuple('State', ['you', 'steps'])
def get_smallest_common_multiplier(w, l):
    i = w + l
    while not (i % w == 0 and i % l == 0):
        i+=1
    return i

def determine_wind_moves(winds: Set[Wind], wcycle: int, rlimit: int, climit: int) -> List[Set]:
    all_moves = list()
    for _ in range(wcycle):
        all_winds = set()
        for wind in winds:
            if wind.direction == Direction.LEFT:
                if wind.col > 1:
                    wind.col -= 1
                else:
                    wind.col = climit - 1
            elif wind.direction == Direction.RIGHT:
                if wind.col < climit - 1:
                    wind.col += 1
                else:
                    wind.col = 1
            elif wind.direction == Direction.UP:
                if wind.row > 1:
                    wind.row -= 1
                else:
                    wind.row = rlimit - 1
            elif wind.direction == Direction.DOWN:
                if wind.row < rlimit - 1:
                    wind.row += 1
                else:
                    wind.row = 1
            all_winds.add((wind.row, wind.col))
        all_moves.append(all_winds)
    return all_moves
        
    

@session.submit_result(level=1, tests=[({'inp': [
    '#.######',
    '#>>.<^<#',
    '#.<..<<#',
    '#>v.><>#',
    '#<^v^^>#',
    '######.#'
]}, 18)])
def solve_part1(inp):
    Entity.all_entities = defaultdict(set)
    
    for r, row in enumerate(inp):
        for c, char in enumerate(row):
            if char == '#':
                Wall(r, c)
            elif char in [dir.value for dir in Direction]:
                Wind(r, c, Direction(char))
                
    
    room_width = len(inp) - 2
    room_length = len(inp[0]) - 2
    wind_cycle = get_smallest_common_multiplier(room_width, room_length)
    
    wind_moves = determine_wind_moves(Entity.all_entities[Wind], wind_cycle,
                                      rlimit=len(inp)-1, climit=len(inp[0])-1)
    
    frontier = deque([State(You(r=0, c=1), 0)])
    wall_positions = {(w.row, w.col) for w in Entity.all_entities[Wall]}
    while frontier:
        you, steps = frontier.popleft()
        wind_move = wind_moves[steps%len(wind_moves)]
        
        open_spaces = you.search_near_open_spaces(wind_move, wall_positions)
        if (room_width, room_length) in open_spaces: # the point before destination
            return steps + 2
        
        for r, c in open_spaces:
            next_state = State(You(r,c), steps+1)
            if next_state not in frontier:
                frontier.append(next_state)
    

@session.submit_result(level=2, tests=[({'inp': [
    '#.######',
    '#>>.<^<#',
    '#.<..<<#',
    '#>v.><>#',
    '#<^v^^>#',
    '######.#'
]}, 54)])
def solve_part2(inp):
    Entity.all_entities = defaultdict(set)
    
    for r, row in enumerate(inp):
        for c, char in enumerate(row):
            if char == '#':
                Wall(r, c)
            elif char in [dir.value for dir in Direction]:
                Wind(r, c, Direction(char))
                
    
    room_width = len(inp) - 2
    room_length = len(inp[0]) - 2
    wind_cycle = get_smallest_common_multiplier(room_width, room_length)
    wind_moves = determine_wind_moves(Entity.all_entities[Wind], wind_cycle,
                                      rlimit=len(inp)-1, climit=len(inp[0])-1)
    
    starting_state = State(You(r=0, c=1), 0)
    steps1 = optimal_steps(starting_state, destination=(room_width, room_length), wind_moves=wind_moves)
    steps2 = optimal_steps(State(You(r=room_width+1, c=room_length), steps1), destination=(1, 1), wind_moves=wind_moves)
    steps3 = optimal_steps(State(You(r=0, c=1), steps2), destination=(room_width, room_length), wind_moves=wind_moves)
    return steps3

def optimal_steps(start, destination, wind_moves):
    frontier = deque([start])
    start_r = start.you.row
    start_c = start.you.col
    
    wall_positions = {(w.row, w.col) for w in Entity.all_entities[Wall]}
    while frontier:
        you, steps = frontier.popleft()
        wind_move = wind_moves[steps%len(wind_moves)]
        
        open_spaces = you.search_near_open_spaces(wind_move, wall_positions)
        
        if destination in open_spaces: # the point before destination
            return steps + 2
        
        for r, c in open_spaces:
            if r == start_r and start_c == c and (you.row != start_r or you.col != start_c):
                continue
            next_state = State(You(r,c), steps+1)
            if next_state not in frontier:
                frontier.append(next_state)
if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
