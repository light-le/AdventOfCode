from collections import namedtuple, deque
from itertools import product
from typing import List
from utils import AdventSession, extract_year_day_from_path
from pprint import pprint

session = AdventSession(**extract_year_day_from_path(__file__))

Position = namedtuple('Position', ['x', 'y', 'z'])

class Cube:
    def __init__(self, position: Position) -> None:
        self.position = position
        
        self.sides = 6
        
    def __ge__(self, __o) -> bool:
        return all(p >= o for p, o in zip(self.position, __o.position))
    
    def __le__(self, __o) -> bool:
        return all(p <= o for p, o in zip(self.position, __o.position))
        
    @classmethod
    def parse_cube(cls, line: str) -> object:
        return cls(Position(*[int(s) for s in line.split(',')]))
    
    def __repr__(self) -> str:
        return str(self.position)
    
    def __eq__(self, __o: object) -> bool:
        return self.position == __o.position
    
    def __hash__(self) -> int:
        return hash(self.position)
    
    def adjacent_cubes(self) -> List[object]:
        cls = self.__class__
        next_cubes = list()
        for d in [-1, 1]:
            next_cubes.append(cls(Position(self.position.x+d, self.position.y, self.position.z)))
            next_cubes.append(cls(Position(self.position.x, self.position.y+d, self.position.z)))
            next_cubes.append(cls(Position(self.position.x, self.position.y, self.position.z+d)))
        return next_cubes
    
    def adjacent_inside_limit(self, min_pos: Position, max_pos: Position) -> List[object]:
        return [cube for cube in self.adjacent_cubes() if cube >= min_pos and cube <= max_pos]

@session.submit_result(level=1, tests=[({'inp': [
    '2,2,2',
    '1,2,2',
    '3,2,2',
    '2,1,2',
    '2,3,2',
    '2,2,1',
    '2,2,3',
    '2,2,4',
    '2,2,6',
    '1,2,5',
    '3,2,5',
    '2,1,5',
    '2,3,5'
]}, 64)])
def solve_part1(inp):
    cubes = {Cube.parse_cube(line) for line in inp}
    
    return get_cube_exposed_sides(cubes)

def get_cube_exposed_sides(cubes):
    exposed_sides = 0
    
    for cube in cubes:
        cube_exposed_sides = cube.sides
        
        for next_cube in cube.adjacent_cubes():
            if next_cube in cubes:
                cube_exposed_sides -= 1
        exposed_sides += cube_exposed_sides
    return exposed_sides

@session.submit_result(level=2, tests=[({'inp': [
    '2,2,2',
    '1,2,2',
    '3,2,2',
    '2,1,2',
    '2,3,2',
    '2,2,1',
    '2,2,3',
    '2,2,4',
    '2,2,6',
    '1,2,5',
    '3,2,5',
    '2,1,5',
    '2,3,5'
]}, 58)])
def solve_part2(inp):
    solid_cubes = {Cube.parse_cube(line) for line in inp}
    
    minx = min(cube.position.x for cube in solid_cubes) - 1
    miny = min(cube.position.y for cube in solid_cubes) - 1
    minz = min(cube.position.z for cube in solid_cubes) - 1
    
    maxx = max(cube.position.x for cube in solid_cubes) + 1
    maxy = max(cube.position.y for cube in solid_cubes) + 1
    maxz = max(cube.position.z for cube in solid_cubes) + 1
    
    min_cube = Cube(Position(minx, miny, minz))
    max_cube = Cube(Position(maxx, maxy, maxz))
    
    water_cubes = {min_cube, max_cube}
    frontier = deque([min_cube, max_cube])
    
    while frontier:
        water_cube = frontier.popleft()
        next_cubes_inlimit = {cube for cube in water_cube.adjacent_inside_limit(min_cube, max_cube)}
        next_water_cubes = next_cubes_inlimit - (next_cubes_inlimit & solid_cubes)
        new_water_cubes = next_water_cubes - (next_water_cubes & water_cubes)

        frontier.extend(list(new_water_cubes))
        water_cubes |= new_water_cubes
        
    all_cubes = {Cube(Position(x, y, z)) for x, y, z in product(range(minx, maxx+1),
                                                                range(miny, maxy+1),
                                                                range(minz, maxz+1))}
    
    air_cubes = all_cubes - water_cubes - solid_cubes
    inner_sides = get_cube_exposed_sides(air_cubes)
    outer_sides = get_cube_exposed_sides(solid_cubes) - inner_sides
    return outer_sides


if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
