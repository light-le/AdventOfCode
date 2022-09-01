from functools import cache
from hashlib import md5
from typing import Callable
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

@cache
def md5_hash(inp: str) -> str:
    return md5(inp.encode()).hexdigest()

@cache
def hash_multiples(inp: str, times=2017) -> str:
    for _ in range(times):
        inp = md5_hash(inp)
    return inp

def has_triple(inp: str) -> str:
    c = 0
    while c < len(inp) - 2:
        if inp[c] == inp[c+1] and inp[c] == inp[c+2]:
            return inp[c]
        c += 1
def solve_part(inp: str, hash_func: Callable) -> int: 
    key_count = 0
    i = -1
    while key_count < 64:
        i+=1
        hash = hash_func(inp+str(i))
        
        tripie = has_triple(hash)
        if tripie:
            pentie = tripie*5
            for j in range(i+1, i+1001):
                hashj = hash_func(inp+str(j))
                if pentie in hashj:
                    key_count += 1
                    break
    return i

@session.submit_result(level=1, tests=[({'inp': 'abc'}, 22728)])
def solve_part1(inp):
    return solve_part(inp, md5_hash)

@session.submit_result(level=2, tests=[({'inp': 'abc'}, 22551)])
def solve_part2(inp):
    return solve_part(inp, hash_multiples)


if __name__ == '__main__':
    inp = session.read_input().rstrip()
    
    solve_part1(inp)
    
    solve_part2(inp)
