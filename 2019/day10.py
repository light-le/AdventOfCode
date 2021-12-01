

from typing import List
from decimal import Decimal


part1_test = [
    (""".#..#
        .....
        #####
        ....#
        ...##""", 8),
    ('''......#.#.
        #..#.#....
        ..#######.
        .#.#.###..
        .#..#.....
        ..#....#.#
        #..#....#.
        .##.#..###
        ##...#..#.
        .#....####''', 33),
    ('''#.#...#.#.
        .###....#.
        .#....#...
        ##.#.#.#.#
        ....#.#.#.
        .##..###.#
        ..#...##..
        ..##....##
        ......#...
        .####.###.''', 35),
    ('''.#..#..###
        ####.###.#
        ....###.#.
        ..###.##.#
        ##.##.#.#.
        ....###..#
        ..#.#..#.#
        #..#.#.###
        .##...##.#
        .....#.#..''', 41),
    ('''.#..##.###...#######
        ##.############..##.
        .#.######.########.#
        .###.#######.####.#.
        #####.##.#.##.###.##
        ..#####..#.#########
        ####################
        #.####....###.#.#.##
        ##.#################
        #####.##.###..####..
        ..######..##.#######
        ####.##.####...##..#
        .#####..#.######.###
        ##...#.##########...
        #.##########.#######
        .####.#.###.###.#.##
        ....##.##.###..#####
        .#.#.###########.###
        #.#.#.#####.####.###
        ###.##.####.##.#..##''', 210)
]

part1_actual = '''..............#.#...............#....#....
                  #.##.......#....#.#..##........#...#......
                  ..#.....#....#..#.#....#.....#.#.##..#..#.
                  ...........##...#...##....#.#.#....#.##..#
                  ....##....#...........#..#....#......#.###
                  .#...#......#.#.#.#...#....#.##.##......##
                  #.##....#.....#.....#...####........###...
                  .####....#.......#...##..#..#......#...#..
                  ...............#...........#..#.#.#.......
                  ........#.........##...#..........#..##...
                  ...#..................#....#....##..#.....
                  .............#..#.#.........#........#.##.
                  ...#.#....................##..##..........
                  .....#.#...##..............#...........#..
                  ......#..###.#........#.....#.##.#......#.
                  #......#.#.....#...........##.#.....#..#.#
                  .#.............#..#.....##.....###..#..#..
                  .#...#.....#.....##.#......##....##....#..
                  .........#.#..##............#..#...#......
                  ..#..##...#.#..#....#..#.#.......#.##.....
                  #.......#.#....#.#..##.#...#.......#..###.
                  .#..........#...##.#....#...#.#.........#.
                  ..#.#.......##..#.##..#.......#.###.......
                  ...#....###...#......#..#.....####........
                  .............#.#..........#....#......#...
                  #................#..................#.###.
                  ..###.........##...##..##.................
                  .#.........#.#####..#...##....#...##......
                  ........#.#...#......#.................##.
                  .##.....#..##.##.#....#....#......#.#....#
                  .....#...........#.............#.....#....
                  ........#.##.#...#.###.###....#.#......#..
                  ..#...#.......###..#...#.##.....###.....#.
                  ....#.....#..#.....#...#......###...###...
                  #..##.###...##.....#.....#....#...###..#..
                  ........######.#...............#...#.#...#
                  ...#.....####.##.....##...##..............
                  ###..#......#...............#......#...#..
                  #..#...#.#........#.#.#...#..#....#.#.####
                  #..#...#..........##.#.....##........#.#..
                  ........#....#..###..##....#.#.......##..#
                  .................##............#.......#..'''

class Asteroid:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        
        self.in_sight = []
        self.not_in_sight = []

    @property
    def views(self):
        return len(self.in_sight)

    def line_equation(self, o):
        m = Decimal(self.y - o.y)/Decimal(self.x - o.x)
        b = self.y - m*self.x
        return m, b

    def inline_check(self, ast1, ast2):
        # special case, vertical line
        if ast1.x == ast2.x:
            return self.x == ast1.x
        m, b = ast1.line_equation(ast2)
        return self.x*m + b == self.y

    def __repr__(self) -> str:
        return f'{self.x} {self.y}'

    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y

    def __str__(self) -> str:
        return str(self.views)


class SpaceMap:
    def __init__(self, smap) -> None:
        self.smap = smap

    def find_asteroids_between(self, ast1: Asteroid, ast2: Asteroid):
        if ast1.x == ast2.x:
            col_space = [row[ast1.x] for row in self.smap]
            return [space for space in col_space[(min(ast1.y, ast2.y)+1):max(ast1.y, ast2.y)] if isinstance(space, Asteroid)]
        elif ast1.y == ast2.y:
            return [space for space in self.smap[ast1.y][(min(ast1.x, ast2.x)+1):max(ast1.x, ast2.x)] if isinstance(space, Asteroid)]
        asters_in_between = []
        for row in self.smap[(min(ast1.y, ast2.y)+1):max(ast1.y, ast2.y)]:
            for space in row[(min(ast1.x, ast2.x)+1):max(ast1.x, ast2.x)]:
                if isinstance(space, Asteroid):
                    asters_in_between.append(space)
        return asters_in_between

    def sight_check(self, asteroids):
        for a1, ast1 in enumerate(asteroids):
            for ast2 in asteroids[a1+1:]:
                if ast1 == ast2 or ast2 in ast1.in_sight or ast2 in ast1.not_in_sight:
                    continue
                in_sight = True
                for ast3 in self.find_asteroids_between(ast1, ast2):
                    if ast3 in ast1.not_in_sight or ast3 in ast2.not_in_sight:
                        continue # not gonna be a blocker
                    if ast3.inline_check(ast1, ast2): # found a blocker
                        ast1.not_in_sight.append(ast2)
                        ast2.not_in_sight.append(ast1)
                        in_sight = False
                        break
                if in_sight:
                    ast1.in_sight.append(ast2)
                    ast2.in_sight.append(ast1)
    
    def __repr__(self) -> str:
        return '\n'.join([''.join([str(space) for space in row]) for row in self.smap])

def solve_part1(inp):
    lines = inp.replace(' ', '').split('\n')
    space_map = SpaceMap([[c for c in row] for row in lines])

    asteroids = []
    for r, row in enumerate(lines):
        for c, space in enumerate(row):
            if space == '#':
                aster = Asteroid(c, r)
                space_map.smap[r][c] = aster
                asteroids.append(aster)
    space_map.sight_check(asteroids)
    # print(space_map)
    max_view = max([ast.views for ast in asteroids])
    # if len(space_map.smap) >= 13:
    #     print(space_map.smap[1][14].in_sight, len(space_map.smap[1][14].in_sight))
    #     print(space_map.smap[1][14].not_in_sight, len(space_map.smap[1][14].not_in_sight))
    #     print(space_map.smap[13][11].in_sight, len(space_map.smap[13][11].in_sight))
    #     print(space_map.smap[13][11].not_in_sight, len(space_map.smap[13][11].not_in_sight))
    # elif len(space_map.smap) < 6:
    #     for aster in asteroids:
    #         print(aster.x, aster.y, aster.in_sight, aster.not_in_sight)
    # for aster in asteroids:
    #     if aster.views == max_view:
    #         print(aster.x, aster.y)
    return max_view
print(solve_part1(part1_actual)) 
# for input_test, output_test in part1_test:
#     cal_output = solve_part1(input_test)
#     assert cal_output == output_test, f"Expected {output_test}, got {cal_output} instead"