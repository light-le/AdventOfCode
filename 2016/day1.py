from collections import namedtuple
from typing import List
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

Instruction = namedtuple('Instruction', ['dir', 'steps'])

class Coordinate:
    dirs = ('N', 'E', 'S', 'W')
    def __init__(self) -> None:
        self._x = 0
        self._y = 0
        
        self.dir = 'N'
        
        self.visited = {(self._x, self._y)}
        self.visited_twice = None

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @x.setter
    def x(self, new_x):
        if new_x > self.x:
            new_points = [(x, self.y) for x in range(self.x+1, new_x+1)]
        elif new_x < self.x:
            new_points = [(x, self.y) for x in range(self.x-1, new_x-1, -1)]
        else:
            raise Exception("Something wrong, new_x and x is the same")
        self.determine_if_visited_twice(new_points)
        self._x = new_x
        
    @y.setter
    def y(self, new_y):
        if new_y > self.y:
            new_points = [(self.x, y) for y in range(self.y+1, new_y+1)]
        elif new_y < self.y:
            new_points = [(self.x, y) for y in range(self.y-1, new_y-1, -1)]
        self.determine_if_visited_twice(new_points)
        self._y = new_y
        
    def determine_if_visited_twice(self, new_points):
        common_points = self.visited & set(new_points)
        if common_points:
            if len(common_points) == 1:
                [self.visited_twice] = common_points
            else:
                for new_point in new_points:
                    if new_point in self.visited:
                        self.visited_twice = new_point
                        break
        else:
            self.visited |= set(new_points)
                
        
    def determine_next_direction(self, dir: str):
        if dir == 'L':
            self.dir = self.dirs[self.dirs.index(self.dir)-1]
        elif dir == 'R':
            new_index = self.dirs.index(self.dir)+1
            if new_index >= len(self.dirs):
                new_index = 0
            self.dir = self.dirs[new_index]
        else:
            raise Exception(f'Invalid instruction direction {dir}')
    
    def follow_instruction(self, ins: Instruction):
        self.determine_next_direction(ins.dir)
        if self.dir == 'N':
            self.y += ins.steps
        elif self.dir == 'S':
            self.y -= ins.steps
        elif self.dir == 'W':
            self.x -= ins.steps
        elif self.dir == 'E':
            self.x += ins.steps
        else:
            raise Exception(f'Invalid direction {self.dir}')
        

        
def parse_instruction(ins: str) -> Instruction:
    dir, *steps = ins
    return Instruction(dir=dir, steps=int(''.join(steps)))

@session.submit_result(level=1,
                       tests=[({'ins': [parse_instruction(d) for d in ['R2', 'L3']]}, 5),
                              ({'ins': [parse_instruction(d) for d in ['R2', 'R2', 'R2']]}, 2),
                              ({'ins': [parse_instruction(d) for d in ['R5', 'L5', 'R5', 'R3']]}, 12)
                             ])
def solve_part1(ins: List):
    you = Coordinate()
    for i in ins:
        you.follow_instruction(i)
    return abs(you.x) + abs(you.y)

@session.submit_result(level=2,
                       tests=[({'ins': list(map(parse_instruction, ['R8', 'R4', 'R4', 'R8']))}, 4),
                              ({'ins': list(map(parse_instruction,
                                                ['R5', 'L2', 'L8', 'R2', 'R4', 'R6']))}, 3),
                              ])
def solve_part2(ins):
    you = Coordinate()
    for i in ins:
        you.follow_instruction(i)
        if you.visited_twice:
            visited_x, visited_y = you.visited_twice
            return abs(visited_x) + abs(visited_y)


if __name__ == '__main__':
    inp = session.read_input().strip()
    instructions = [parse_instruction(ins) for ins in inp.split(', ') if ins]

    solve_part1(instructions)
    
    solve_part2(instructions)
