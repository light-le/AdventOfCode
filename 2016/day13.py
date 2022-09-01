
from collections import deque, namedtuple
from typing import Iterable
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

Point = namedtuple("Point", ['x', 'y'])

class Maze:
    def __init__(self, fav_n: int) -> None:
        self.cubicles = dict()
        self.favorite_n = fav_n
        
    def check_valid(self, p: Point) -> bool:
        if p in self.cubicles:
            return self.cubicles[p]

        x = p.x
        y = p.y
        s = x*x + 3*x + 2*x*y + y + y*y + self.favorite_n
        b1_count = bin(s).count('1')
        
        self.cubicles[p] = (b1_count % 2 == 0)
        return self.cubicles[p]
        
        
class Explorer:
    visited = set()
    step50_count = 0

    def __init__(self, coor: Point, steps:int=0) -> None:
        self.coor = coor
        self.steps = steps
        self.visited.add(coor)
    
    def find_surrounding_empty_spaces(self, maze: Maze) -> Iterable[Point]:
        sur_points = set()
        if self.coor.y > 0:
            up = Point(self.coor.x, self.coor.y-1)
            if maze.check_valid(up) and up not in self.visited:
                sur_points.add(up)
        if self.coor.x > 0:
            left = Point(self.coor.x-1, self.coor.y)
            if maze.check_valid(left) and left not in self.visited:
                sur_points.add(left)
                
        right = Point(self.coor.x+1, self.coor.y)
        if maze.check_valid(right) and right not in self.visited:
            sur_points.add(right)
            
        down = Point(self.coor.x, self.coor.y+1)
        if maze.check_valid(down) and down not in self.visited:
            sur_points.add(down)
        
        return sur_points


@session.submit_result(level=1)
def solve_part1(maze):
    
    frontier = deque([Explorer(Point(1,1))])
    
    while frontier:
        exp = frontier.popleft()
        if exp.coor == Point(31, 39):
            return exp.steps
        possible_move_points = exp.find_surrounding_empty_spaces(maze)
        frontier.extend([Explorer(point, exp.steps+1) for point in possible_move_points])
        
@session.submit_result(level=2)
def solve_part2(maze):
    frontier = deque([Explorer(Point(1,1))])
    location50_count = 0
    while frontier:
        exp = frontier.popleft()
        location50_count += 1
        if exp.steps < 50:
            possible_move_points = exp.find_surrounding_empty_spaces(maze)
            frontier.extend([Explorer(point, exp.steps+1) for point in possible_move_points])
    return location50_count
            
        

if __name__ == '__main__':
    inp = session.read_input()
    
    maze = Maze(fav_n=int(inp))
    solve_part1(maze)
    
    solve_part2(maze)
