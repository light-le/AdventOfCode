
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

@session.submit_result(level=1, tests=[({'inp': [
    '1000',
    '2000',
    '3000',
    '',
    '4000',
    '',
    '5000',
    '6000',
    '',
    '7000',
    '8000',
    '9000',
    '',
    '10000',
]}, 24000)])
def solve_part1(inp):
    totals = total_calories_each_elf(inp)
    
    return max(totals)

def total_calories_each_elf(inp):
    totals = list()
    subtotal = 0
    for calorie in inp:
        if calorie == '':
            totals.append(subtotal)
            subtotal = 0
        else:
            subtotal += int(calorie)
    totals.append(subtotal)
    return totals

@session.submit_result(level=2, tests=[({'inp': [
    '1000',
    '2000',
    '3000',
    '',
    '4000',
    '',
    '5000',
    '6000',
    '',
    '7000',
    '8000',
    '9000',
    '',
    '10000',
]}, 45000)])
def solve_part2(inp):
    totals = total_calories_each_elf(inp)
    sorted_totals = sorted(totals)
    return sum(sorted_totals[-3:])


if __name__ == '__main__':
    inp = session.read_input().split('\n')
    
    solve_part1(inp)
    
    solve_part2(inp)
