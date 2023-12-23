from __future__ import annotations
from collections import namedtuple, deque
from dataclasses import dataclass, field
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

BrickEnd = namedtuple('BrickEnd', ['x', 'y', 'z'])

@dataclass
class Brick:
    left_end: BrickEnd
    right_end: BrickEnd
    supported_by: set=field(default_factory=set, init=False, repr=False)
    supporting: set=field(default_factory=set, repr=False, init=False)
    collapsed: bool=False
    
    def __repr__(self) -> str:
        return f'Left {self.left_end.x}, {self.left_end.y}, {self.left_end.z}. Right {self.right_end.x}, {self.right_end.y}, {self.right_end.z}'
    
    def __hash__(self) -> int:
        return hash((self.left_end, self.right_end))
    
    def __eq__(self, __value: Brick) -> bool:
        return self.left_end == __value.left_end and self.right_end == __value.right_end
    
    def _check_initial_coordinates(self) -> None:
        assert [
            self.left_end.z == self.right_end.z,
            self.left_end.x == self.right_end.x, 
            self.left_end.y == self.right_end.y
        ].count(True) >= 2, f'Wrong ends {self.left_end} {self.right_end}'
        
    def __post_init__(self) -> None:
        self._check_initial_coordinates()
        
    @property
    def height(self) -> int:
        return abs(self.left_end.z - self.right_end.z) + 1
        
    @classmethod
    def parse_line(self, line:str) -> Brick:
        left_str, right_str = line.split('~')
        left_coors = [int(s) for s in left_str.split(',')]
        right_coors = [int(s) for s in right_str.split(',')]
        return Brick(left_end=BrickEnd(*left_coors), right_end=BrickEnd(*right_coors))
    
class Space(list):
    '''Basically a 3D list, or a list within a list within a list, init with max x and y'''
    def __init__(self, max_x: int, max_y: int) -> None:
        '''Create ground (#) as first level'''
        ground = [['#' for _ in range(max_x)] for _ in range(max_y)]
        self._max_x = max_x
        self._max_y = max_y
        super().__init__([ground])
    
    def __repr__(self) -> str:
        print_out = ''
        for l, level in enumerate(self):
            print_out += f'\nLevel {l}\n'
            print_out += '\n'.join([''.join(row) for row in level])
        return print_out
    
    @property
    def height(self) -> int:
        '''Not counting ground level, this also represents the highest level'''
        return len(self) - 1
    
    def add_empty_levels(self, l: int=1) -> None:
        [self.add_empty_level() for _ in range(l)]
        
    def add_empty_level(self) -> None:
        self.append([['.' for _ in range(self._max_x)] for _ in range(self._max_y)])
    
    def add_brick(self, brick: Brick) -> None:
        if brick.left_end.z != brick.right_end.z: # vertical brick (same x and same y)
            brick_x = brick.left_end.x
            brick_y = brick.left_end.y
            
            overtrude_height = brick.height
            low_level = self.height
            high_level = self.height
            while overtrude_height: # TODO: redo this
                if self[low_level][brick_y][brick_x] == '.':
                    overtrude_height -= 1
                    low_level -= 1
                    self[low_level][brick_y][brick_x] = brick
                else:
                    self.add_empty_level()
                    high_level += 1
                    self[high_level][brick_y][brick_x] = brick
                    overtrude_height -= 1
                    
            if self[low_level][brick_y][brick_x] != '#':
                brick.supported_by.add(self[low_level][brick_y][brick_x])
        else:
            min_x, max_x = sorted([brick.left_end.x, brick.right_end.x])
            min_y, max_y = sorted([brick.left_end.y, brick.right_end.y])
            brick_xy = {(x, y) for x in range(min_x, max_x+1) for y in range(min_y, max_y+1)}
            
class Ground:
    pass

class Level:
    def __init__(self, max_x: int, max_y: int) -> None:
        self.level_heights = [[(Ground, 0) for _ in range(max_x)] for _ in range(max_y)]
        
    def add_brick(self, brick: Brick) -> None:
        bmax_x = max(brick.left_end.x, brick.right_end.x)
        bmin_x = min(brick.left_end.x, brick.right_end.x)
        bmax_y = max(brick.left_end.y, brick.right_end.y)
        bmin_y = min(brick.left_end.y, brick.right_end.y)
        
        brick_xy = {(x, y) for x in range(bmin_x, bmax_x+1) for y in range(bmin_y, bmax_y+1)}
        
        level_heights = [self.level_heights[y][x] for x, y in brick_xy]
        _, max_height = max(level_heights, key=lambda lh: lh[1])
        
        height_after_fall = max_height + brick.height
        
        for x, y in brick_xy:
            under_obj, under_height = self.level_heights[y][x]
            if isinstance(under_obj, Brick) and under_height == max_height:
                brick.supported_by.add(under_obj)
                under_obj.supporting.add(brick)
                
            self.level_heights[y][x] = (brick, height_after_fall)


@session.submit_result(level=1, tests=[({'inp': [
    '1,0,1~1,2,1',
    '0,0,2~2,0,2',
    '0,2,3~2,2,3',
    '0,0,4~0,2,4',
    '2,0,5~2,2,5',
    '0,1,6~2,1,6',
    '1,1,8~1,1,9'
]}, 5)], wrong_answers={5, 963})
def solve_part1(inp: list[str]):
    bricks = [Brick.parse_line(line) for line in inp]
    
    sorted_bricks = sorted(bricks, key=lambda b: min(b.left_end.z, b.right_end.z))
    max_x = max([brick.left_end.x for brick in bricks] + [brick.right_end.x for brick in bricks])
    max_y = max([brick.left_end.y for brick in bricks] + [brick.right_end.y for brick in bricks])
    
    levels = Level(max_x+1, max_y+1)
    
    for brick in sorted_bricks:
        levels.add_brick(brick)

    sole_supporting_brick = set()
    for brick in bricks:
        # print(brick, brick.supported_by)
        if len(brick.supported_by) == 1:
            sole_supporting_brick |= brick.supported_by
    return len(bricks) - len(sole_supporting_brick)
            


@session.submit_result(level=2, tests=[({'inp': [
    '1,0,1~1,2,1',
    '0,0,2~2,0,2',
    '0,2,3~2,2,3',
    '0,0,4~0,2,4',
    '2,0,5~2,2,5',
    '0,1,6~2,1,6',
    '1,1,8~1,1,9'
]}, 7)], wrong_answers={
    66942, # too low
})
def solve_part2(inp: list[str]):
    bricks = [Brick.parse_line(line) for line in inp]
    
    sorted_bricks = sorted(bricks, key=lambda b: min(b.left_end.z, b.right_end.z))
    max_x = max([brick.left_end.x for brick in bricks] + [brick.right_end.x for brick in bricks])
    max_y = max([brick.left_end.y for brick in bricks] + [brick.right_end.y for brick in bricks])
    
    levels = Level(max_x+1, max_y+1)
    
    for brick in sorted_bricks:
        levels.add_brick(brick)

    total_collapsed = 0
    
    for brick in bricks:
        for brick2 in bricks:
            brick2.collapsed = False
            
        brick.collapsed = True
        collapsed_bricks = {brick}
        frontier = deque(brick.supporting)
        # visited_bricks = brick.supporting
        
        while frontier:
            brickin = frontier.popleft()
            if not (brickin.supported_by - collapsed_bricks):
                brickin.collapsed = True
                collapsed_bricks.add(brickin)
                
                frontier.extend(list(brickin.supporting))
        total_collapsed += (len(collapsed_bricks)-1)
    return total_collapsed
            

if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
