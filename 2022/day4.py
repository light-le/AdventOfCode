
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

@session.submit_result(level=1, tests=[({'inp': [
    '2-4,6-8',
    '2-3,4-5',
    '5-7,7-9',
    '2-8,3-7',
    '6-6,4-6',
    '2-6,4-8'
]}, 2)])
def solve_part1(inp):
    contain_count = 0
    for pair in inp:
        e1, e2 = pair.split(',')
        e1min, e1max = [int(s) for s in e1.split('-')]
        e2min, e2max = [int(s) for s in e2.split('-')]
        
        if e1min >= e2min:
            if e1max <= e2max:
                contain_count += 1
                continue
        if e2min >= e1min:
            if e2max <= e1max:
                contain_count += 1
    
    return contain_count

@session.submit_result(level=2, tests=[({'inp': [
    '2-4,6-8',
    '2-3,4-5',
    '5-7,7-9',
    '2-8,3-7',
    '6-6,4-6',
    '2-6,4-8'
]}, 4)])
def solve_part2(inp):
    overlap_count = 0
    for pair in inp:
        e1, e2 = pair.split(',')
        e1min, e1max = [int(s) for s in e1.split('-')]
        e2min, e2max = [int(s) for s in e2.split('-')]

        if not (e1max < e2min or e2max < e1min):
            overlap_count += 1
            
    return overlap_count


if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
