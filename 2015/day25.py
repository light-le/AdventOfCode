from functools import cache
from re import findall
from utils import AdventSession, extract_year_day_from_path

N = 20151125
MULTIPLIER = 252533
DIVISOR = 33554393

@cache
def find_code_at(r, c) -> int:
    diags_before = r + c - 2
    
    loops = (diags_before+1)*diags_before//2 + c - 1
    n = N
    for _ in range(loops):
        n = (n*MULTIPLIER) % DIVISOR
    return n
    

if __name__ == '__main__':
    session = AdventSession(**extract_year_day_from_path(__file__))
    
    inp = session.read_input().strip()
    row, col = [int(s) for s in findall('\d+', inp)]
    
    assert find_code_at(6, 5) == 1534922
    assert find_code_at(3, 4) == 7981243
    assert find_code_at(5, 2) == 17552253
    
    part1_answer = find_code_at(row, col)
    print(part1_answer)
    session.post_answer(part1_answer, level=1)