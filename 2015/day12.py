from typing import Dict, List
from utils import AdventSession, extract_year_day_from_path
import re
import json

def solve_part1(input: str) -> int:
    all_numbers = re.findall('-?\d+', input)
    return sum([int(num) for num in all_numbers])

def evaluate_dict(d: Dict):
    if 'red' in d.values():
        return 0
    total = 0
    for key, value in d.items():
        if isinstance(value, int):
            total += value
        elif isinstance(value, list):
            total += evaluate_list(value)
        elif isinstance(value, dict):
            total += evaluate_dict(value)
        elif isinstance(value, str):
            pass
        else:
            raise Exception(f'Unexpected type {key, value}')
    return total

def evaluate_list(l: List):
    total = 0
    for item in l:
        if isinstance(item, int):
            total += item
        elif isinstance(item, list):
            total += evaluate_list(item)
        elif isinstance(item, dict):
            total += evaluate_dict(item)
        elif isinstance(item, str):
            pass
        else:
            raise Exception(f'Unexpected type {type(item)}')
    return total

def solve_part2(input: str) -> int:
    book = json.loads(input)
    return evaluate_list(book)

if __name__ == '__main__':
    session = AdventSession(**extract_year_day_from_path(__file__))

    input = session.read_input()

    part1_answer = solve_part1(input)
    print(part1_answer)
    session.post_answer(part1_answer, level=1)

    part2_answer = solve_part2(input)
    print(part2_answer)
    session.post_answer(part2_answer, level=2)