from collections import namedtuple
from copy import deepcopy
from utils import AdventSession, extract_year_day_from_path

SIZE = 100
Point = namedtuple('Point', ['x', 'y'])
FOUR_CORNERS = {Point(0, 0), Point(0, SIZE-1), Point(SIZE-1, 0), Point(SIZE-1, SIZE-1)}


class Light:
    grid = [[None for _ in range(SIZE)] for _ in range(SIZE)]

    def __init__(self, state: str, point: Point) -> None:
        if state == '#':
            self.on = True
        elif state == '.':
            self.on = False
        else:
            raise Exception(f'Invalid light state {state}')
        
        self.point = point
        self.neighbors = set()
        
        cls = self.__class__
        cls.grid[point.y][point.x] = self
        
        for px in range(point.x-1, point.x+2):
            if px < 0 or px >= SIZE:
                continue
            for py in range(point.y-1, point.y+2):
                if py < 0 or py >= SIZE or (px == point.x and py == point.y):
                    continue
                neighbor = cls.grid[py][px]
                if neighbor:
                    self.neighbors.add(neighbor)
                    neighbor.neighbors.add(self)

        
    def __hash__(self) -> int:
        return hash(self.point)
    
    def __repr__(self) -> str:
        return f'{self.point}, {self.on}'
    
    def __str__(self) -> str:
        return '#' if self.on else '.'

def run_100steps(grid, disable_4corners=False):
    for step in range(100):
        switches = set()
        for y, line in enumerate(grid):
            for x, light in enumerate(line):
                if disable_4corners and light.point in FOUR_CORNERS:
                    continue

                on_neighbors = len({neig for neig in light.neighbors if neig.on})
                if light.on:
                    if on_neighbors not in {2,3}:
                        switches.add((Point(x, y), False))
                else:
                    if on_neighbors == 3:
                        switches.add((Point(x, y), True))
        for point, state in switches:
            grid[point.y][point.x].on = state

    return sum(len([light for light in line if light.on]) for line in grid)
            
def fabricate_grid(grid, four_corners_on=False):
    Light.grid = [[None for _ in range(SIZE)] for _ in range(SIZE)]
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if four_corners_on and Point(x, y) in FOUR_CORNERS:
                char = '#'
            Light(char, Point(x, y))
    return Light.grid
        
    

if __name__ == '__main__':
    session = AdventSession(**extract_year_day_from_path(__file__))
    
    grid = [line for line in session.read_input().split('\n') if line]
    
    part1_answer = run_100steps(fabricate_grid(grid))
    print(part1_answer)
    session.post_answer(part1_answer, level=1)
   
    part2_answer = run_100steps(fabricate_grid(grid, four_corners_on=True), disable_4corners=True)
    print(part2_answer)
    session.post_answer(part2_answer, level=2)
    