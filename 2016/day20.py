
from collections import namedtuple
from typing import List
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

Range = namedtuple('Range', ['small', 'big'])

def parse_black_list(txt: str) -> Range:
    small, big = txt.split('-')
    return Range(int(small), int(big))

@session.submit_result(level=1, tests=[
    ({'ranges': [Range(5, 8), Range(0, 2), Range(4, 7)]}, 3),
    ({'ranges': [Range(0, 4), Range(3, 8), Range(10, 12)]}, 9)
    ])
def solve_part1(ranges: List[Range]):
    sorted_range = sorted(ranges, key=lambda r: r.small)
    first_range = sorted_range.pop(0)
    for range in sorted_range:
        if range.small <= first_range.big + 1:
            first_range = Range(first_range.small, max(first_range.big, range.big))
        else:
            return first_range.big+1

def part2_solution2(ranges: List[Range], maxn: int=4294967295) -> int:
    sorted_range = sorted(ranges, key=lambda r: r.small)
    first_range = sorted_range.pop(0)
    
    blockeds = first_range.big - first_range.small + 1
    
    for range in sorted_range:
        if range.small <= first_range.big+1:
            if range.big > first_range.big:
                blockeds += (range.big - first_range.big)
                first_range = Range(first_range.small, range.big)
        else:
            blockeds += (range.big - range.small + 1)
            first_range = range
    
    alloweds = maxn + 1 - blockeds
    return alloweds
    

@session.submit_result(level=2, tests=[
    ({'ranges': [Range(5, 8), Range(0, 2), Range(4, 7)], 'maxn': 9}, 2),
    ({'ranges': [Range(0, 4), Range(3, 8), Range(10, 12)], 'maxn': 15}, 4),
    ({'ranges': [Range(1, 7), Range(3, 6), Range(8, 10)], 'maxn': 12}, 3),
])
def solve_part2(ranges, maxn = 4294967295):
    return part2_solution2(ranges, maxn)


if __name__ == '__main__':
    ranges = [parse_black_list(inp) for inp in session.read_input().split('\n') if inp]
    solve_part1(ranges)
    
    solve_part2(ranges)
