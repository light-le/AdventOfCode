from typing import List
from string import ascii_uppercase
from collections import namedtuple
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

Procedure = namedtuple('Procedure', ['n', 'from_', 'to'])

def parse_procedure(p):
    move, n, fr, from_, t, to = p.split()
    return Procedure(n=int(n), from_=int(from_), to=int(to))
    

@session.submit_result(level=1, tests=[({'config': {
    1: ['Z', 'N'],
    2: ['M', 'C', 'D'],
    3: ['P']
    },
    'procedures': [
        'move 1 from 2 to 1',
        'move 3 from 1 to 3',
        'move 2 from 2 to 1',
        'move 1 from 1 to 2',    
    ]}, 'CMZ')])
def solve_part1(config, procedures):
    procs = [parse_procedure(p) for p in procedures]
    for proc in procs:
        for _ in range(proc.n):
            config[proc.to].append(config[proc.from_].pop())
    
    tops = ''.join([crates[-1] for crates in config.values()])
    return tops

@session.submit_result(level=2, tests=[({'config': {
    1: ['Z', 'N'],
    2: ['M', 'C', 'D'],
    3: ['P']
    },
    'procedures': [
        'move 1 from 2 to 1',
        'move 3 from 1 to 3',
        'move 2 from 2 to 1',
        'move 1 from 1 to 2',    
    ]}, 'MCD')])
def solve_part2(config, procedures):
    procs = [parse_procedure(p) for p in procedures]
    for proc in procs:
        to_move = config[proc.from_][-proc.n:]
        config[proc.from_] = config[proc.from_][:-proc.n]
        config[proc.to].extend(to_move)
    
    tops = ''.join([crates[-1] for crates in config.values()])
    return tops

def parse_config(c: str) -> List[str]:
    rows = c.split('\n')
    
    crate_nums = rows[-1].split()
    crate_configs = {
        int(num): list() for num in crate_nums
    }
    
    for crate_row in rows[::-1]:
        for c, char in enumerate(crate_row):
            if char in ascii_uppercase:
                crate_configs[(c+3)//4].append(char)
        
    return crate_configs
        


if __name__ == '__main__':
    init, proc = session.read_input().split('\n\n')
    
    config = parse_config(init)
    
    procedures = proc.split('\n')[:-1]
    
    solve_part1({num: li.copy() for num, li in config.items()}, procedures)

    solve_part2({num: li.copy() for num, li in config.items()}, procedures)
    