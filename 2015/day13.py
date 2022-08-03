from functools import cache
from itertools import combinations, permutations
from typing import Dict
from utils import AdventSession, extract_year_day_from_path

test_input = '''Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.'''

test_output = 330

class Person:
    all_people = dict()
    def __init__(self, name) -> None:
        self.name = name
        self.friends = dict()
        
    def add_friend(self, name, happy_points: int):
        self.friends[name] = happy_points
    
    def __hash__(self) -> int:
        return hash(self.name)
    
    @classmethod
    def add_if_not_exist(cls, name: str):
        if name not in cls.all_people:
            person = Person(name)
            cls.all_people[name] = person
        else:
            person = cls.all_people[name]
        return person

    @classmethod
    def parse_happiness_rule(cls, rule: str):
        name, would, gain_lose, happy_point, *_, other = rule.split(' ')
        other = other[:-1]  # remove the dot at the end
        
        person = Person.add_if_not_exist(name)
        other_person = Person.add_if_not_exist(other)
        
        person.add_friend(other, int(happy_point) if gain_lose == 'gain'
                                                  else -int(happy_point))
        return person
        
    def __repr__(self) -> str:
        return f'{self.name} friends are {self.friends}'

class SeatingArrangement(tuple):
    happy_book = Person.all_people

    def rotate_right(self):
        return SeatingArrangement((self[-1],) + self[:-1])
    
    def reverse(self):
        return SeatingArrangement(self[::-1])
    
    @cache
    def calculate_happiness(self) -> int:
        if len(self) == 3:
            three_combs = combinations(self, 2)
            three_sum = sum(self.calculate_pair_happiness(pa, pb) for pa, pb in three_combs)
            return three_sum
        return (
            SeatingArrangement(self[:-1]).calculate_happiness()
            - self.calculate_pair_happiness(self[0], self[-2])
            + self.calculate_pair_happiness(self[0], self[-1])
            + self.calculate_pair_happiness(self[-2], self[-1])
        )
    
    def calculate_pair_happiness(self, pa: str, pb: str) -> int:
        if pa == 'You' or pb == 'You':
            return 0
        return (
            self.happy_book[pa].friends[pb]
            + self.happy_book[pb].friends[pa]
        )
    
def simplify_arrangements(arrs: set) -> set:
    '''
    Input {'ABCD', 'ADBC', 'BCDA', 'CDAB', 'DCBA'}
    Output {'ABCD', 'ADBC'}
    '''
    simplified = set()
    while arrs:
        arr = arrs.pop()
        simplified.add(arr)
        reversed_arr = arr.reverse()
        arrs.discard(reversed_arr)

        for _ in range(len(arr)-1):
            arr = arr.rotate_right()
            arrs.discard(arr)
            
            reversed_arr = reversed_arr.rotate_right()
            arrs.discard(reversed_arr)
    return simplified

def optimal_happiness(names) -> int:
    seating_arrangements = {SeatingArrangement(arr) for arr in permutations(names, len(names))}
    unique_arrangements = simplify_arrangements(seating_arrangements)
    happiness = [arr.calculate_happiness() for arr in unique_arrangements]
    
    max_happiness = max(happiness)
    
    return max_happiness

def test_part1(inp: str, opt: int):
    rules = [rule for rule in inp.split('\n')]
    [Person.parse_happiness_rule(rule) for rule in rules]
    output = optimal_happiness(set(Person.all_people.keys()))
    
    assert output == opt

def solve_part2():
    Person.add_if_not_exist('You')
    return optimal_happiness(set(Person.all_people.keys()))
    
if __name__ == '__main__':
    test_part1(test_input, test_output)
    
    session = AdventSession(**extract_year_day_from_path(__file__))
    rules = [rule for rule in session.read_input().split('\n') if rule]
    
    [Person.parse_happiness_rule(rule) for rule in rules]
    
    all_names = set(Person.all_people.keys())
    part1_answer = optimal_happiness(all_names)
    print(part1_answer)
    session.post_answer(part1_answer, level=1)
    
    part2_answer = solve_part2()
    print(part2_answer)
    session.post_answer(part2_answer, level=2)