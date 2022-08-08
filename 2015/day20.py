from typing import Set
from utils import AdventSession, extract_year_day_from_path

def find_divisors(n: int) -> Set[int]:
    divisors = set()
    for i in range(1, int(n**0.5)+1):
        if n % i == 0:
            divisors |= {i, n//i}
    return divisors


def solve_part1(inp: int) -> int:
    max_house_no = inp//(2*10)
    presents = [0] + [10 for _ in range(max_house_no)]
    for hn in range(2, max_house_no+1):
        for hi in range(hn, max_house_no+1, hn):
            presents[hi] += hn*10
        if presents[hn] >= inp:
            return hn

def solve_part2(inp: int) -> int:
    max_house_no = inp//(2*11)
    presents = [0] + [11 for _ in range(max_house_no)]
    for hn in range(2, max_house_no+1):
        for hi in range(hn, min(hn*50+1, max_house_no+1), hn):
            presents[hi] += hn*11
        if presents[hn] >= inp:
            return hn
    
if __name__ == '__main__':
    session = AdventSession(**extract_year_day_from_path(__file__))
    
    inp = int(session.read_input().strip())
    
    part1_answer = solve_part1(inp)
    print(part1_answer)
    session.post_answer(part1_answer, level=1)
    
    part2_answer = solve_part2(inp)
    print(part2_answer)
    session.post_answer(part2_answer, level=2)