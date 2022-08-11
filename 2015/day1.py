from collections import Counter
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

@session.submit_result(level=1)
def solve_part1(line):
    counter = Counter(line)
    return counter['('] - counter[')']

@session.submit_result(level=2)
def solve_part2(line):
    floor = 0
    for c, char in enumerate(line):
        if char == '(':
            floor+=1
        elif char == ')':
            floor-=1
        else:
            raise Exception(f'Invalid character {char}')

        if floor == -1:
            return c
        
if __name__ == '__main__':
    line = session.read_input().strip()
    solve_part1(line)
    solve_part2(line)