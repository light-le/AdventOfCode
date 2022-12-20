from typing import List, Tuple
from collections import namedtuple
from itertools import cycle
from abc import ABC, abstractmethod
from pprint import pprint
from datetime import datetime

from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

Position = namedtuple('Position', ['x', 'y'])

class Shape(ABC):
    def __init__(self, points: List[Position]) -> None:
        self.points = points
        
    @property
    def leftmost_xrel(self) -> int:
        return 0
    
    @property
    def rightmost_xrel(self) -> int:
        return max(p.x for p in self.points)
    
    @property
    def bottom_points(self) -> List[Position]:
        '''
        For a set of points in each x, get the point with lowest y
        '''
        all_x = [p.x for p in self.points]
        return [min([p for p in self.points if p.x == x],
                    key=(lambda p: p.y)) for x in range(min(all_x), max(all_x)+1)]
        
    def __repr__(self) -> str:
        return self.__class__.__name__
    
    def __eq__(self, __o: object) -> bool:
        return repr(self) == repr(__o)
        
    @property
    def yrange(self) -> range:
        ys = [p.y for p in self.points]    
        return range(min(ys), max(ys)+1)
    
    @property
    def right_edge(self) -> List[Position]:
        '''
        For a set of points in each y, get the point with highest x
        '''
        return [max([p for p in self.points if p.y == y],
                    key=(lambda p: p.x)) for y in self.yrange]
        
    @property
    def left_edge(self) -> List[Position]:
        '''
        For a set of points in each y, get the point with lowest x
        '''
        return [min([p for p in self.points if p.y == y],
                    key=(lambda p: p.x)) for y in self.yrange]
        
class Minus(Shape):
    def __init__(self) -> None:
        super().__init__([Position(x, 0) for x in range(4)])
        
class Plus(Shape):
    def __init__(self) -> None:
        super().__init__([Position(0, 1), Position(1, 0), Position(2, 1), Position(1, 1), Position(1, 2)])
        
class L(Shape):
    def __init__(self) -> None:
        super().__init__([Position(x, 0) for x in range(3)] + [Position(2, y) for y in range(1, 3)])
    
class Column(Shape):
    def __init__(self) -> None:
        super().__init__([Position(0, y) for y in range(4)])
        
class Square(Shape):
    def __init__(self) -> None:
        super().__init__([Position(0, 0), Position(1, 0), Position(0, 1), Position(1, 1)])
    
class Rock:
    def __init__(self, shape: Shape, position_y: int) -> None:
        self.is_resting = False
        self.shape = shape
        self.position = Position(x=2, y=position_y)
        
    def __repr__(self) -> str:
        return f'Rock {self.is_resting} resting at position {self.position} and abs points {self.absolute_points}'
        
    @property
    def leftmost_x(self) -> int:
        return self.shape.leftmost_xrel + self.position.x
    
    @property
    def rightmost_x(self) -> int:
        return self.shape.rightmost_xrel + self.position.x
    
    def is_touching_right_wall(self):
        return self.rightmost_x == 6
    
    def is_touching_left_wall(self):
        return self.leftmost_x == 0
    
    def shift_right(self):
        self.position = Position(self.position.x+1, self.position.y)
    
    def shift_left(self):
        self.position = Position(self.position.x-1, self.position.y)
        
    def shift_down(self):
        self.position = Position(self.position.x, self.position.y-1)
    
    def is_anything_beneath(self, tower: List[List[str]]):
        for bottom_point in self.shape.bottom_points:
            absy = self.position.y + bottom_point.y
            absx = self.position.x + bottom_point.x
            if len(tower) >= absy:
                if tower[absy-1][absx] == '#':
                    return True
        return False
    
    def is_anything_on_right(self, tower: List[List[str]]):
        for right_point in self.shape.right_edge:
            absy = self.position.y + right_point.y
            absx = self.position.x + right_point.x
            if absx == (len(tower[0])-1):
                return True # touching right wall
            elif absx > (len(tower[0])-1):
                raise Exception(f'Not possible to have rock with x {absx} on rightwall')

            if len(tower) > absy:
                # print(absx, absy, tower[absy])
                if tower[absy][absx+1] == '#':
                    return True
        return False

    def is_anything_on_left(self, tower: List[List[str]]):
        for left_point in self.shape.left_edge:
            absy = self.position.y + left_point.y
            absx = self.position.x + left_point.x
            if absx == 0:
                return True # touching left wall
            elif absx < 0:
                raise Exception(f'Not possible to have rock with x {absx} on leftwall')

            if len(tower) > absy:
                if tower[absy][absx-1] == '#':
                    return True
        return False
            
    
    @property
    def absolute_points(self) -> List[Position]:
        return [Position(self.position.x + shape_point.x,
                         self.position.y + shape_point.y) for shape_point in self.shape.points]
    
    def rest(self, tower: List[List[str]]) -> None:
        self.is_resting = True
        for abs_point in sorted(self.absolute_points, key=(lambda p: (p.y, p.x))):
            if len(tower) == abs_point.y:
                tower.append(['.' for _ in range(7)])
            elif len(tower) < abs_point.y:
                raise Exception(f'Not possible to have tower height {len(tower)} < point y{abs_point.y}')
            
            tower[abs_point.y][abs_point.x] = '#'
        
        
@session.submit_result(level=1, tests=[({'inp': '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'}, 3068)])
def solve_part1(inp):
    
    tower = [['#' for _ in range(7)]]
    
    wind_dirs = cycle(inp)
    rock_shapes = cycle([Minus(), Plus(), L(), Column(), Square()])
    
    for rc in range(2022):
        height = len(tower) - 1
        rock = Rock(shape=next(rock_shapes), position_y=height+4)
        
        while not rock.is_resting:
            wind_dir = next(wind_dirs)
            if wind_dir == '>' and not rock.is_anything_on_right(tower):
                rock.shift_right()
            elif wind_dir == '<' and not rock.is_anything_on_left(tower):
                rock.shift_left()

            if not rock.is_anything_beneath(tower):
                rock.shift_down()
            else:
                rock.rest(tower)
            
    return len(tower)-1
                
                
        
        
    

@session.submit_result(level=2, print_only=True) # tests=[({'inp': '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'}, 1514285714288)])
def solve_part2(inp):
    tower = [['#' for _ in range(7)]]
    
    wind_length = len(inp)
    print(wind_length)
    w = 0
    
    rock_shapes = cycle([Minus(), Plus(), L(), Column(), Square()])
    special_rock = 0

    for rc in range(10**6):
        
        height = len(tower) - 1
        rock = Rock(shape=next(rock_shapes), position_y=height+4)
        
        while not rock.is_resting:
            wind_dir = inp[w]

            w+=1
            if w == wind_length:
                w = 0
                special_rock = 753
                # print(rock.position, rock.position.y - (len(tower)-1))

            if wind_dir == '>' and not rock.is_anything_on_right(tower):
                rock.shift_right()
            elif wind_dir == '<' and not rock.is_anything_on_left(tower):
                rock.shift_left()

            if not rock.is_anything_beneath(tower):
                rock.shift_down()
            else:
                rock.rest(tower)
                if special_rock > 0:
                    if special_rock == 1:
                        print(rc, rock.shape, rock.position, len(tower)-1)
                    special_rock-=1
                    
                    
    return len(tower)-1


if __name__ == '__main__':
    inp = session.read_input()[:-1]
    
    solve_part1(inp)
    
    before = datetime.now()
    solve_part2(inp)
    print((datetime.now() - before).seconds, 'secs')
