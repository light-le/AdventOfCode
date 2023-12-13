
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

def check_rows_symmetry(rows: list[str], r: int) -> bool:
    upper = rows[:r+1]
    lower = rows[r+1:]
    
    size = min(len(upper), len(lower))
    upper = upper[(len(upper)-size):]
    lower_flipped = lower[:size][::-1]
    return upper == lower_flipped
    
    

@session.submit_result(level=1, tests=[({'inp': [
'''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.''',

'''#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''
]}, 405)])
def solve_part1(inp: list[str]):
    total = 0
    for a, area in enumerate(inp):
        rows = area.split('\n')
        if rows[-1] == '':
            rows.pop()
        
        for r, row in enumerate(rows[:-1]):
            if row == rows[r+1]:
                symmetrical_row = check_rows_symmetry(rows, r)
                if symmetrical_row:
                    total += (r+1)*100
        
        cols = [[row[i] for row in rows] for i in range(len(rows[0]))]
        for c, col in enumerate(cols[:-1]):
            if col == cols[c+1]:
                symmetrical_col = check_rows_symmetry(cols, c)
                if symmetrical_col:
                    total += (c+1)
        print(f'finished area {a}')
    return total

def is_different_by_1(u: list[str], l: list[str]) -> bool:
    false_count = 0
    for ru, rl in zip(u, l):
        false_count += [charu == charl for charu, charl in zip(ru, rl)].count(False)
        if false_count > 1:
            return False
    return false_count == 1

def check_rows_symmetry_with_smudge(rows: list[str], r) -> bool:
    upper = rows[:r+1]
    lower = rows[r+1:]
    
    size = min(len(upper), len(lower))
    upper = upper[(len(upper)-size):]
    lower_flipped = lower[:size][::-1]
    
    return is_different_by_1(upper, lower_flipped)
@session.submit_result(level=2, tests=[({'inp': [
'''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.''',

'''#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''
]}, 400)])
def solve_part2(inp: list[str]):
    total = 0
    for a, area in enumerate(inp):
        rows = area.split('\n')
        if rows[-1] == '':
            rows.pop()
        
        for r, row in enumerate(rows[:-1]):
            if [r1 == r2 for r1, r2 in zip(row, rows[r+1])].count(False) <= 1:
                symmetrical_row = check_rows_symmetry_with_smudge(rows, r)
                if symmetrical_row:
                    total += (r+1)*100
        
        cols = [[row[i] for row in rows] for i in range(len(rows[0]))]
        for c, col in enumerate(cols[:-1]):
            if [c1 == c2 for c1, c2 in zip(col, cols[c+1])].count(False) <= 1:
                symmetrical_col = check_rows_symmetry_with_smudge(cols, c)
                if symmetrical_col:
                    total += (c+1)
    return total


if __name__ == '__main__':
    inp = session.read_input().split('\n\n')
    
    solve_part1(inp)
    
    solve_part2(inp)
