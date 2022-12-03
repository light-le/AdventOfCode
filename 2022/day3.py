
from utils import AdventSession, extract_year_day_from_path
from string import ascii_lowercase, ascii_uppercase

session = AdventSession(**extract_year_day_from_path(__file__))

priorities = {letter: i+1 for i, letter in enumerate(ascii_lowercase+ascii_uppercase)}

def find_common_char(s1: str, s2: str):
    return list(set(s1) & set(s2))

def find_common_char_in_group(g: list[str]):
    return list(set(g[0]) & set(g[1]) & set(g[2]))

@session.submit_result(level=1, tests=[({'inp': [
    'vJrwpWtwJgWrhcsFMMfFFhFp',
    'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
    'PmmdzqPrVvPwwTWBwg',
    'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
    'ttgJtRGJQctTZtZT',
    'CrZsJsPPZsGzwwsLwLmpwMDw',
]}, 157)])
def solve_part1(inp):
    points = 0
    for rucksack in inp:
        common_items = find_common_char(rucksack[:len(rucksack)//2], rucksack[len(rucksack)//2:])
        if common_items:
            [common_item] = common_items
            points += priorities[common_item]
    return points

@session.submit_result(level=2, tests=[({'inp': [
    'vJrwpWtwJgWrhcsFMMfFFhFp',
    'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
    'PmmdzqPrVvPwwTWBwg',
    'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
    'ttgJtRGJQctTZtZT',
    'CrZsJsPPZsGzwwsLwLmpwMDw',
]}, 70)])
def solve_part2(inp):
    
    group = ['', '', '']
    points = 0
    for r, rucksack in enumerate(inp):
        group[r%3] = rucksack
        if r%3==2:
            common_items = find_common_char_in_group(group)
            if common_items:
                [common_item] = common_items
                points+= priorities[common_item]
    return points


if __name__ == '__main__':
    inp = session.read_input().split('\n')
    
    solve_part1(inp)
    
    solve_part2(inp)
