
from collections import defaultdict
from functools import reduce
from typing import List

from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class Triangle:
    def __init__(self, *sizes: int) -> None:
        self.sizes = sizes
        small, mid, large = sorted(sizes)
        
        self.isvalid = (small+mid) > large
    
    def __repr__(self) -> str:
        return str(self.sizes)
            
    @classmethod
    def parse_sizes(cls, line: str):
        return cls(*list(map(int, line.split())))

count_valid_triangles = lambda ts: len([t for t in ts if t.isvalid])

@session.submit_result(level=1, tests=[({'triangles': [
    Triangle(5, 10, 25),
    Triangle(8, 4, 10),
    Triangle(2, 4, 9),
    Triangle(15, 3, 14),
    Triangle(18, 5, 10),
]}, 2)])
def solve_part1(triangles):
    return count_valid_triangles(triangles)


def pivot_row_by_3(rows: List[str]):
    pivoteds = defaultdict(lambda: [[0, 0, 0] for _ in range (3)])
    
    for r, row in enumerate(rows):
        sizes = list(map(int, row.split()))
        by3 = r // 3
        remainer3 = r % 3
        for s, size in enumerate(sizes):
            pivoteds[by3][s][remainer3] = size
            
    return reduce((lambda a,b: a + b), list(pivoteds.values()))
        
def test_pivot_row_by_3():
    inp = [
        '101 301 501',
        '102 302 502',
        '103 303 503',
        '201 401 601',
        '202 402 602',
        '203 403 603',
    ]
    expected_ouput = [
        [101, 102, 103],
        [301, 302, 303],
        [501, 502, 503],
        [201, 202, 203],
        [401, 402, 403],
        [601, 602, 603]
    ]
    output = pivot_row_by_3(inp)
    assert output == expected_ouput, f'Calculated output: {output}'

@session.submit_result(level=2, tests=[({'inp': [
    '5  10   25',
    '8   4   10',
    '2 4    9',
    '15   3     14',
    '18  5     10',
    '11    3   7',
]}, 3)])
def solve_part2(inp):
    test_pivot_row_by_3()
    pivoteds = pivot_row_by_3(inp)
    triangles = [Triangle(*sizes) for sizes in pivoteds]
    return count_valid_triangles(triangles)

if __name__ == '__main__':
    inp = [i for i in session.read_input().split('\n') if i]
    triangles = list(map(Triangle.parse_sizes, inp))
    
    solve_part1(triangles)
    
    solve_part2(inp)
