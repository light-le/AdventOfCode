from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, field
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class Direction(Enum):
    RIGHT = 1
    DOWN = -2
    LEFT = -1
    UP = 2
    def flip(self) -> Direction:
        return Direction(-self.value)
        

@dataclass
class Node:
    row: int
    col: int
    is_excited: bool=field(init=False, default=False)
    # light_from: Direction=field(init=False, default=None)
    # light_to: Direction=field(init=False, default=None)
    light_dirs: set[Direction]=field(init=False, default_factory=set)
    
    def copy(self) -> Node:
        return self.__class__(row=self.row, col=self.col)
    
    def _compute_next_light_position(self, light_to: Direction) -> tuple[int, int]:
        if light_to == Direction.DOWN:
            return (self.row+1, self.col)
        elif light_to == Direction.UP:
            return (self.row-1, self.col)
        elif light_to == Direction.RIGHT:
            return (self.row, self.col+1)
        elif light_to == Direction.LEFT:
            return (self.row, self.col-1)
        else:
            raise Exception(f'light_to is {light_to}')
    
    def _compute_light_to(self, light_from: Direction) -> None:
        return [light_from.flip()]
    
    # def get_next_light_positions(self) -> list[tuple[int, int, Direction]]:
    #     self._compute_light_to()
    #     return [self._compute_next_light_position() + (self.light_to,)]
    def get_next_light_positions(self, light_from: Direction) -> list[tuple[int, int, Direction]]:
        return [self._compute_next_light_position(light_to) + (light_to,) for light_to in self._compute_light_to(light_from)]
    

class ForwardMirror(Node):
    FORWARD_MIRROR_FROM_TO = {
        Direction.LEFT: Direction.UP,
        Direction.UP: Direction.LEFT,
        Direction.DOWN: Direction.RIGHT,
        Direction.RIGHT: Direction.DOWN
    }
    def _compute_light_to(self, light_from: Direction) -> list[Direction]:
        return [self.FORWARD_MIRROR_FROM_TO[light_from]]

class BackwardMirror(Node):
    BACKWARD_MIRROR_FROM_TO = {
        Direction.LEFT: Direction.DOWN,
        Direction.DOWN: Direction.LEFT,
        Direction.UP: Direction.RIGHT,
        Direction.RIGHT: Direction.UP
    }
    def _compute_light_to(self, light_from: Direction) -> list[Direction]:
        return [self.BACKWARD_MIRROR_FROM_TO[light_from]]
        
class VerticalSpliter(Node):
    def _compute_light_to(self, light_from: Direction) -> list[Direction]:
        if light_from in (Direction.UP, Direction.DOWN):
            return [Direction(-light_from.value)]
        elif light_from in (Direction.LEFT, Direction.RIGHT):
            return [Direction.UP, Direction.DOWN]
        else:
            raise Exception(f'Invalid light_from {light_from}')
            

class HorizontalSpliter(Node):
    def _compute_light_to(self, light_from: Direction) -> list[Direction]:
        if light_from in (Direction.UP, Direction.DOWN):
            return [Direction.LEFT, Direction.RIGHT]
        elif light_from in (Direction.LEFT, Direction.RIGHT):
            return [Direction(-light_from.value)]
        else:
            raise Exception(f'Invalid light_from {light_from}')
            
        
    

OBJECTS = {
    '.': Node,
    '/': ForwardMirror,
    '\\': BackwardMirror,
    '|': VerticalSpliter,
    '-': HorizontalSpliter
}


@session.submit_result(level=1, tests=[({'inp': [
    '.|...\....',
    '|.-.\.....',
    '.....|-...',
    '........|.',
    '..........',
    '.........\\',
    '..../.\\\\..',
    '.-.-/..|..',
    '.|....-|.\\',
    '..//.|....'
]}, 46)])
def solve_part1(inp: list[str]):
    map = []
    for l, line in enumerate(inp):
        row = []
        for c, char in enumerate(line):
            row.append(OBJECTS[char](l, c))
        map.append(row)
    
    light0 = map[0][0]
    light_from = Direction.LEFT
    return count_excited_lights(map, light0, light_from)

def count_excited_lights(map, light0, light_from):
    light0.is_excited = True
    light0.light_dirs.add(light_from)
    exciment_count = 1
    lights = [(light0, light_from)]
    while lights:
        node, light_from = lights.pop()
        next_light_positions = node.get_next_light_positions(light_from)
        
        for next_light_row, next_light_col, next_light_dir in next_light_positions:
            if not 0 <= next_light_row < len(map) or not 0 <= next_light_col < len(map[0]):
                continue
            
            next_light = map[next_light_row][next_light_col]
            
            if not next_light.is_excited:
                exciment_count += 1
            elif next_light_dir.flip() in next_light.light_dirs:
                continue # another light have passed thru this path in this direction before
            

            next_light.is_excited = True
            next_light_from = next_light_dir.flip()
            next_light.light_dirs.add(next_light_from)

            lights.append((next_light, next_light_from))
    
    return exciment_count
            
def print_map_exciment(map: list[list[Node]]):    
    for row in map:
        print_outs = []
        for node in row:
            if node.is_excited:
                print_outs.append('#')
            else:
                print_outs.append('.')
        print(''.join(print_outs)) 
        

@session.submit_result(level=2, tests=[({'inp': [
    '.|...\....',
    '|.-.\.....',
    '.....|-...',
    '........|.',
    '..........',
    '.........\\',
    '..../.\\\\..',
    '.-.-/..|..',
    '.|....-|.\\',
    '..//.|....'
]}, 51)])
def solve_part2(inp: list[str]):
    map = [[OBJECTS[char](l, c) for c, char in enumerate(line)] for l, line in enumerate(inp)]
    
    starting_positions_direction = (
        [(node.row, node.col, Direction.UP) for node in map[0]] +
        [(node.row, node.col, Direction.DOWN) for node in map[-1]] +
        [(node.row, node.col, Direction.LEFT) for node in [row[0] for row in map]] +
        [(node.row, node.col, Direction.RIGHT) for node in [row[-1] for row in map]]
    )
    
    max_excited_nodes = 0
    
    for starting_row, starting_col, starting_dir in starting_positions_direction:
        new_map = [[node.copy() for node in row] for row in map]
        starting_light = new_map[starting_row][starting_col]
        excited_count = count_excited_lights(new_map, starting_light, starting_dir)
        max_excited_nodes = max(max_excited_nodes, excited_count)
    return max_excited_nodes


if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
