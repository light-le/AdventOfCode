from itertools import product
from functools import cache
from collections import deque
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

def check_validity(marks: str, counts: list[int]) -> bool:
    '''check of the counts would match the list of marks'''
    mark_lists = marks.replace('.', ' ').split()
    if len(mark_lists) != len(counts):
        return False
    return all([len(marks) == c for marks, c in zip(mark_lists, counts)])

def replace_long_string_with_long_string(marks: str, replacement: str) -> str:
    list_of_marks = list(marks)
    r = 0
    for m, mark in enumerate(list_of_marks):
        if mark == '?':
            list_of_marks[m] = replacement[r]
            r += 1
    return ''.join(list_of_marks)


def count_arrangements(mark: str, counts: list[int]) -> int:
    line_arrangements = 0
    
    qmark_count = mark.count('?')
    all_possible_combs = product('.#', repeat=qmark_count)
    for combi in all_possible_combs:
        str_replacement = replace_long_string_with_long_string(mark, ''.join(combi))
        if check_validity(str_replacement, counts):
            line_arrangements += 1
            
    return line_arrangements


@session.submit_result(level=1, tests=[({'inp': [
    '???.### 1,1,3',
    '.??..??...?##. 1,1,3',
    '?#?#?#?#?#?#?#? 1,3,1,6',
    '????.#...#... 4,1,1',
    '????.######..#####. 1,6,5',
    '?###???????? 3,2,1'
]}, 21)])
def solve_part1(inp: list[str]):
    possible_arrangements = 0
    for line in inp:
        mark, count_str = line.split(' ')
        counts = [int(s) for s in count_str.split(',')]
        line_arrangements = count_arrangements(mark, counts)
        possible_arrangements += line_arrangements
        
    return possible_arrangements

@cache
def count_arrangements_recursively(mark: str, counts: tuple[int]):
    if not counts:
        if set(mark) <= {'.', '?'}:
            return 1
        else:
            return 0
    if len(mark) < (sum(counts)+len(counts)-1):
        return 0
    
    arrangements = 0
    acount = counts[0]
    
    i = 0
    while i < len(mark):
        if (i+acount <= len(mark) and  # make sure it doesn't go overboard
            set(mark[i:i+acount]) <= {'?', '#'} and # make sure there's no '.' in between
            (i+acount == len(mark) or mark[i+acount] in ('.', '?')) and # make sure it ends or has . at end
            (i == 0 or mark[i-1] in ('.', '?'))): # make sure it at the beginning or has . before
            
            arrangements += count_arrangements_recursively(mark[i+acount+1:], counts[1:])
        if mark[i] == '#':
            break
        i+=1
    
    return arrangements

@session.submit_result(level=2, tests=[({'inp': [
    '???.### 1,1,3',
    '.??..??...?##. 1,1,3',
    '?#?#?#?#?#?#?#? 1,3,1,6',
    '????.#...#... 4,1,1',
    '????.######..#####. 1,6,5',
    '?###???????? 3,2,1'
]}, 525152)])
def solve_part2(inp: list[str]):
    possible_arrangements = 0
    for l, line in enumerate(inp, start=1):
        mark, count_str = line.split(' ')
        counts = [int(s) for s in count_str.split(',')]
        
        assert count_arrangements(mark, counts) == count_arrangements_recursively(mark, tuple(counts)), \
            f'Something wrong at line {l} with {mark} and {counts}'
        
        arrangments = count_arrangements_recursively('?'.join([mark]*5), tuple(counts*5))
        print(f'Finished {l} of {len(inp)} with {arrangments} arrangements')
        possible_arrangements += arrangments
    return possible_arrangements

if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
