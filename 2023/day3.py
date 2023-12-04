
from utils import AdventSession, extract_year_day_from_path
from collections import defaultdict

session = AdventSession(**extract_year_day_from_path(__file__))

@session.submit_result(level=1, tests=[({'inp': [
    '467..114..',
    '...*......',
    '..35..633.',
    '......#...',
    '617*......',
    '.....+.58.',
    '..592.....',
    '......755.',
    '...$.*....',
    '.664.598..'
]}, 4361)])
def solve_part1(inp: list[str]):
    width = len(inp[0])
    height = len(inp)

    part_numbers = []
    for l, line in enumerate(inp):
        num = ''
        num_i = []
        for c, char in enumerate(line):
            if char.isdigit():
                num += char
                num_i.append(c)
            
            if num and (not char.isdigit() or c == width - 1):
                for row in range(max(0, l-1), min(height-1, l+2)):
                    for col in range(max(0, num_i[0]-1), min(width-1, num_i[-1]+2)):
                        if not (inp[row][col].isdigit() or inp[row][col] == '.'):
                            part_numbers.append(int(num))
                num = ''
                num_i = []
    return sum(part_numbers)
                
                

@session.submit_result(level=2, tests=[({'inp': [
    '467..114..',
    '...*......',
    '..35..633.',
    '......#...',
    '617*......',
    '.....+.58.',
    '..592.....',
    '......755.',
    '...$.*....',
    '.664.598..'
]}, 467835)])
def solve_part2(inp: list[str]):
    width = len(inp[0])
    height = len(inp)
    
    numbers = defaultdict(list)
    cores = list()
    
    for l, line in enumerate(inp):
        num = ''
        num_i = []

        for c, char in enumerate(line):
            if char.isdigit():
                num += char
                num_i.append(c)
            elif char == '*':
                cores.append((l, c))
    
            if num and (not char.isdigit() or c == width-1):
                numbers[int(num)].extend([(row, col) for row in range(max(0, l-1), min(height, l+2)) for col in range(max(0, num_i[0]-1), min(num_i[-1]+2, width))])
                
                num = ''
                num_i = []
    core_ratios = []
    for core in cores:
        core_gears = []
        for number, surroundings in numbers.items():
            num_count_around_core = surroundings.count(core)
            if 0 < num_count_around_core < 3:
                core_gears.extend([number]*num_count_around_core)
                if len(core_gears) > 2:
                    break
        if len(core_gears) == 2:
            core_ratios.append(core_gears[0]*core_gears[1])
    return sum(core_ratios)
                
if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
