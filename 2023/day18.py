from collections import namedtuple
from utils import AdventSession, extract_year_day_from_path

from matplotlib import pyplot as plt
session = AdventSession(**extract_year_day_from_path(__file__))

Point = namedtuple('Point', ['row', 'col', 'shape'])

def parse_line(line: str) -> tuple[str, int, str]:
    dir, stepstr, color = line.split()
    steps = int(stepstr)
    hex = color.replace('(#', '').replace(')', '')
    return dir, steps, hex

def parse_inputs(inp: list[str]) -> list[tuple[str, int, str]]:
    return [parse_line(line) for line in inp]

@session.submit_result(level=1, tests=[({'inp': [
    'R 6 (#70c710)',
    'D 5 (#0dc571)',
    'L 2 (#5713f0)',
    'D 2 (#d2c081)',
    'R 2 (#59c680)',
    'D 2 (#411b91)',
    'L 5 (#8ceee2)',
    'U 2 (#caa173)',
    'L 1 (#1b58a2)',
    'U 2 (#caa171)',
    'R 2 (#7807d2)',
    'U 3 (#a77fa3)',
    'L 2 (#015232)',
    'U 2 (#7a21e3)'
]}, 62)])
def solve_part1(inp: list[str]):
    lines = parse_inputs(inp)
    dirs = [line[0] for line in lines]
    stepl = [line[1] for line in lines]
    
    trenches = get_trench_points(dirs, stepl)
    
    loop_dict = {(p.row, p.col): p.shape for p in trenches}
    
    max_row = max(p.row for p in trenches)
    max_col = max(p.col for p in trenches)
    min_row = min(p.row for p in trenches)
    min_col = min(p.col for p in trenches)
    
    lava_cubes = 0
    for r in range(min_row, max_row+1):
        for c in range(min_col, max_col+1):
            if (r, c) in loop_dict:
                lava_cubes += 1
                continue
            
            north_pointers = 0
            for next_c in range(c+1, max_col+1):
                if loop_dict.get((r, next_c)) in {'L', 'J', '|'}:
                    north_pointers += 1
            lava_cubes += (north_pointers % 2)
    return lava_cubes

def get_trench_points(dirs, stepl, corners_only: bool=False):
    trenches = []
    point = Point(0, 0, '-')
    
    next_dirs = dirs[1:] + [dirs[0]]
    for dir, steps, next_dir in zip(dirs, stepl, next_dirs):
        if dir == 'R':
            if not corners_only:
                new_points = [Point(point.row, c, '-') for c in range(point.col+1, point.col+steps)]
            if next_dir == 'U':
                corner_shape = 'J'
            elif next_dir == 'D':
                corner_shape = '7'
            corner_point = Point(point.row, point.col+steps, corner_shape)
        elif dir == 'U':
            if not corners_only:
                new_points = [Point(r, point.col, '|') for r in range(point.row-1, point.row-steps, -1)]
            if next_dir == 'R':
                corner_shape = 'F'
            elif next_dir == 'L':
                corner_shape = '7'
            corner_point = Point(point.row-steps, point.col, corner_shape)
        elif dir == 'L':
            if not corners_only:
                new_points = [Point(point.row, c, '-') for c in range(point.col-1, point.col-steps, -1)]
            if next_dir == 'U':
                corner_shape = 'L'
            elif next_dir == 'D':
                corner_shape = 'F'
            corner_point = Point(point.row, point.col-steps, corner_shape)
        elif dir == 'D':
            if not corners_only:
                new_points = [Point(r, point.col, '|') for r in range(point.row+1, point.row+steps)]
            if next_dir == 'R':
                corner_shape = 'L'
            elif next_dir == 'L':
                corner_shape = 'J'
            corner_point = Point(point.row+steps, point.col, corner_shape)
        else:
            raise Exception(f'Invalid dir {dir}')

        if corners_only:
            new_points = [corner_point]
        else:
            new_points.append(corner_point)

        point = corner_point
        trenches.extend(new_points)
    return trenches
            
def parse_hex(hex: str) -> tuple[str, int]:
    hex_to_dir = {
        '0': 'R',
        '1': 'D',
        '2': 'L',
        '3': 'U'
    }
    
    step_hex = hex[:-1]
    dir_hex = hex[-1]
    return int(step_hex, 16), hex_to_dir[dir_hex]
    
def parse_hexes(hexes: list[str]) -> list[tuple[str, int]]:
    return [parse_hex(hex) for hex in hexes]

def polyplot(points: tuple[int, int]) -> None:
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]

    # Plotting the points and connecting them in order to form a polygon
    plt.figure(figsize=(6, 6))
    plt.plot(x_coords, y_coords, marker='o')
    plt.plot(x_coords, y_coords, linestyle='-', color='b')  # Connect points with lines
    plt.title('Polygon from Given Points')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid(True)
    plt.show()

def polygonArea(vertices: list[tuple[int, int]]) -> int:
  #A function to apply the Shoelace algorithm
  numberOfVertices = len(vertices)
  sum1 = 0
  sum2 = 0
  
  for i in range(0,numberOfVertices-1):
    sum1 = sum1 + vertices[i][0] *  vertices[i+1][1]
    sum2 = sum2 + vertices[i][1] *  vertices[i+1][0]
  
  #Add xn.y1
  sum1 = sum1 + vertices[numberOfVertices-1][0]*vertices[0][1]   
  #Add x1.yn
  sum2 = sum2 + vertices[0][0]*vertices[numberOfVertices-1][1]   
  
  area = abs(sum1 - sum2) / 2
  return int(area)

def compute_perimeter(vertices: list[tuple[int, int]]) -> int:
    point = vertices[0]
    perimeter = point[0] + point[1]
    
    for next_point in vertices[1:]:
        perimeter += abs(next_point[1] - point[1]) + abs(next_point[0] - point[0])
        point = next_point
    return perimeter
        

@session.submit_result(level=2, tests=[({'inp': [
    'R 6 (#70c710)',
    'D 5 (#0dc571)',
    'L 2 (#5713f0)',
    'D 2 (#d2c081)',
    'R 2 (#59c680)',
    'D 2 (#411b91)',
    'L 5 (#8ceee2)',
    'U 2 (#caa173)',
    'L 1 (#1b58a2)',
    'U 2 (#caa171)',
    'R 2 (#7807d2)',
    'U 3 (#a77fa3)',
    'L 2 (#015232)',
    'U 2 (#7a21e3)'
]}, 952408144115)], wrong_answers={
    64294263158490 # too low
})
def solve_part2(inp: list[str]):
    lines = parse_inputs(inp)
    hexes = [line[2] for line in lines]
    
    instructions = parse_hexes(hexes)
    
    steps = [ins[0] for ins in instructions]
    dirs = [ins[1] for ins in instructions]

    trenches = get_trench_points(dirs, steps, corners_only=True)
    
    perimeter = compute_perimeter([(p.row, p.col) for p in trenches])
    
    polyarea = polygonArea([(p.row, p.col) for p in trenches[::-1]])
    
    return polyarea + perimeter//2 + 1
    

if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    solve_part1(inp)
    
    solve_part2(inp)
