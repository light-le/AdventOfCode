
from collections import Counter
from functools import reduce
from typing import List
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

@session.submit_result(level=1, tests=[({'inp': [
    'eedadn',
    'drvtee',
    'eandsr',
    'raavrd',
    'atevrs',
    'tsrnev',
    'sdttsa',
    'rasrtv',
    'nssdts',
    'ntnada',
    'svetve',
    'tesnvt',
    'vntsnd',
    'vrdear',
    'dvrsen',
    'enarar',
    ]}, 'easter')])
def solve_part1(inp):
    cols = pivot_input(inp)
    most_counts = [Counter(col).most_common(1) for col in cols]
    return reduce((lambda a, b: a+b[0][0]), most_counts[1:], most_counts[0][0][0])

def pivot_input(inp: List[str]) -> List[List]:
    cols = []
    for c in range(len(inp[0])):
        cols.append([s[c] for s in inp])
    return cols

@session.submit_result(level=2, tests=[({'inp': [
    'eedadn',
    'drvtee',
    'eandsr',
    'raavrd',
    'atevrs',
    'tsrnev',
    'sdttsa',
    'rasrtv',
    'nssdts',
    'ntnada',
    'svetve',
    'tesnvt',
    'vntsnd',
    'vrdear',
    'dvrsen',
    'enarar',
    ]}, 'advent')])
def solve_part2(inp):
    cols = pivot_input(inp)
    least_counts = [Counter(col).most_common()[-1] for col in cols]
    return reduce((lambda a, b: a+b[0]), least_counts[1:], least_counts[0][0])


if __name__ == '__main__':
    inp = [i for i in session.read_input().split('\n') if i]
    solve_part1(inp)
    
    solve_part2(inp)
