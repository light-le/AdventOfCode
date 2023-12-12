from pprint import pprint
from collections import namedtuple
from itertools import combinations
from utils import AdventSession, extract_year_day_from_path

Point = namedtuple('Point', ['row', 'col'])

session = AdventSession(**extract_year_day_from_path(__file__))

def transpose(l: list[list[str]]) -> list[list[str]]:
    return [[row[i] for row in l] for i in range(len(l[0]))]

def add_empty_rows(universe: list[list[str]]) -> None:
    r = 0
    while r < len(universe):
        row = universe[r]
        if set(row) == {'.'}:
            universe.insert(r, row)
            r+=1
        r+=1
            

def expand_(universe: list[list[str]]) -> None:
    add_empty_rows(universe)
    universe_t = transpose(universe)
    add_empty_rows(universe_t)
    return transpose(universe_t)
    
def get_all_galaxy_points(universe: list[list[str]]) -> list[Point]:
    all_galaxies = []
    for r, row in enumerate(universe):
        for c, char in enumerate(row):
            if char == '#':
                all_galaxies.append(Point(row=r, col=c))
    return all_galaxies
                

@session.submit_result(level=1, tests=[({'inp': [
    '...#......',
    '.......#..',
    '#.........',
    '..........',
    '......#...',
    '.#........',
    '.........#',
    '..........',
    '.......#..',
    '#...#.....'
]}, 374)])
def solve_part1(inp: list[str]):
    universe = [list(line) for line in inp]
    expanded_universe = expand_(universe)
    
    points = get_all_galaxy_points(expanded_universe)
    point_combinations = combinations(points, r=2)
    return sum([abs(p1.row - p2.row) + abs(p1.col - p2.col) for p1, p2 in point_combinations])
    
def distance_between(p1: Point, p2: Point, empty_rows: list[int], empty_cols: list[int], scale: int) -> int:
    '''
    Findout howmany empty rows between p1 and p2, then add (scale-1) for each of them to the abs diff
    Same thing for empty cols
    '''
    empty_rows_between = [r for r in empty_rows if min(p1.row, p2.row) < r < max(p1.row, p2.row)]
    empty_cols_between = [c for c in empty_cols if min(p1.col, p2.col) < c < max(p1.col, p2.col)]
    return int(abs(p1.row-p2.row)+abs(p1.col-p2.col)+(len(empty_rows_between)+len(empty_cols_between))*(scale-1))

@session.submit_result(level=2, tests=[({'inp': [
    '...#......',
    '.......#..',
    '#.........',
    '..........',
    '......#...',
    '.#........',
    '.........#',
    '..........',
    '.......#..',
    '#...#.....'
], 'scale': 2}, 374), ({'inp': [
    '...#......',
    '.......#..',
    '#.........',
    '..........',
    '......#...',
    '.#........',
    '.........#',
    '..........',
    '.......#..',
    '#...#.....'
], 'scale': 10}, 1030), ({'inp': [
    '...#......',
    '.......#..',
    '#.........',
    '..........',
    '......#...',
    '.#........',
    '.........#',
    '..........',
    '.......#..',
    '#...#.....'
], 'scale': 100}, 8410)])
def solve_part2(inp: list[str], scale: int=1e6):
    universe = [list(line) for line in inp]
    empty_rows = [r for r, row in enumerate(universe) if set(row) == {'.'}]
    
    universe_t = transpose(universe)
    empty_cols = [r for r, row in enumerate(universe_t) if set(row) == {'.'}]
    
    points = get_all_galaxy_points(universe)
    
    point_combinations = combinations(points, r=2)
    return sum([distance_between(p1, p2, empty_rows, empty_cols, scale) for p1, p2 in point_combinations])


if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
