from typing import Dict, List
from collections import deque
from utils import AdventSession, extract_year_day_from_path

def parse_transformation(ts: List[str]) -> Dict:
    transbook = dict()
    
    for t in ts:
        before, after = t.split(' => ')
        transbook.setdefault(before, [])
        transbook[before].append(after)

    return transbook


def solve_part1(moles, book):
    c = 0
    new_moles = set()
    while c < len(moles):
        char = moles[c]
        char2 = moles[c:c+2]
        if char in book:
            [new_moles.add(moles[:c]+new_element+moles[c+1:]) for new_element in book[char]]
        elif char2 in book:
            [new_moles.add(moles[:c]+new_element+moles[c+2:]) for new_element in book[char2]]
        c+=1
    return len(new_moles)

def reverse_transformation_book(transbook: Dict) -> Dict:
    reversed_book = dict()
    for key, values in transbook.items():
        for value in values:
            if value in reversed_book:
                raise Exception(f'Duplicated key {value}')
            reversed_book[value] = key
    return reversed_book

def solve_part2(start, end, transbook):
    frontier = deque([(start, 0)])
    old_moles = {start}
    while frontier:
        mole, step = frontier.popleft()
        step += 1
        new_moles = set()
        
        for key, value in transbook.items():
            c = 0
            kl = len(key)
            while c <= len(mole)-kl:
                char = mole[c:c+kl]
                if char == key:
                    new_mole = mole[:c] + value + mole[c+kl:]
                    if new_mole == end:
                        return step
                    new_moles.add((new_mole, step))
                    c+=kl
                else:
                    c+=1
        new_moles -= old_moles
        old_moles |= new_moles
        frontier.extend(new_moles)
        frontier = deque(sorted(frontier, key=lambda x: len(x[0])))
                
                    

if __name__ == '__main__':
    session = AdventSession(**extract_year_day_from_path(__file__))
    
    inp = [ip for ip in session.read_input().split('\n') if ip]
    
    *transformations, molecules = inp
    transbook = parse_transformation(transformations)
    
    part1_answer = solve_part1(molecules, transbook)
    print(part1_answer)
    session.post_answer(part1_answer, level=1)
    
    reversed_book = reverse_transformation_book(transbook)
    part2_answer = solve_part2(start=molecules, end='e', transbook=reversed_book)
    print(part2_answer)
    session.post_answer(part2_answer, level=2)
    
    