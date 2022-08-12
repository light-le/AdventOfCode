from collections import defaultdict
from typing import List, Union
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class KeyPad:
    key_relations = defaultdict(dict)
    reverse_dir = {
        'U': 'D',
        'D': 'U',
        'L': 'R',
        'R': 'L',
    }
    def __init__(self, part=1) -> None:
        if part == 1:
            self.add_key_relation(1, 'R', 2)
            self.add_key_relation(1, 'D', 4)
            self.add_key_relation(2, 'R', 3)
            self.add_key_relation(2, 'D', 5)
            self.add_key_relation(3, 'D', 6)
            self.add_key_relation(4, 'R', 5)
            self.add_key_relation(4, 'D', 7)
            self.add_key_relation(5, 'R', 6)
            self.add_key_relation(5, 'D', 8)
            self.add_key_relation(6, 'D', 9)
            self.add_key_relation(7, 'R', 8)
            self.add_key_relation(8, 'R', 9)
        elif part == 2:
            [self.add_key_relation(key, dir, next_key) for key, dir, next_key in {
                ('1', 'D', '3'),
                ('2', 'D', '6'),
                ('2', 'R', '3'),
                ('3', 'D', '7'),
                ('3', 'R', '4'),
                ('4', 'D', '8'),
                ('5', 'R', '6'),
                ('6', 'R', '7'),
                ('6', 'D', 'A'),
                ('7', 'D', 'B'),
                ('7', 'R', '8'),
                ('8', 'D', 'C'),
                ('8', 'R', '9'),
                ('A', 'R', 'B'),
                ('B', 'D', 'D'),
                ('B', 'R', 'C'),
            }]
        
        self.fulfill_all_key_relations()
        
     
    @classmethod
    def add_key_relation(cls, key: Union[int, str], dir: str, next_key: int):
        cls.key_relations[key][dir] = next_key
        reversed_dir = cls.reverse_dir[dir]
        
        if reversed_dir not in cls.key_relations[next_key]:
            cls.key_relations[next_key][reversed_dir] = key
        
    @classmethod
    def fulfill_all_key_relations(cls):
        for key, relations in cls.key_relations.items():
            for dir in cls.reverse_dir:
                if dir not in relations:
                    cls.key_relations[key][dir] = key
                

@session.submit_result(level=1, tests=[({'inp': ['ULL', 'RRDDD', 'LURDL', 'UUUUD']}, '1985')])
def solve_part1(inp: List):
    keypad = KeyPad()
    start_key = 5
    bath_code = ''
    for dirs in inp:
        for char in dirs:
            start_key = keypad.key_relations[start_key][char]
        bath_code += str(start_key)
    return bath_code

@session.submit_result(level=2, tests=[({'inp': ['ULL', 'RRDDD', 'LURDL', 'UUUUD']}, '5DB3')])
def solve_part2(inp):
    keypad = KeyPad(part=2)
    start_key = '5'
    bath_code = ''
    for dirs in inp:
        for char in dirs:
            start_key = keypad.key_relations[start_key][char]
        bath_code += str(start_key)
    return bath_code


if __name__ == '__main__':
    inp = [i for i in session.read_input().split('\n') if i]
    
    solve_part1(inp)
    
    solve_part2(inp)
