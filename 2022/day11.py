from typing import List
from abc import ABC, abstractmethod
from functools import cache
from collections import deque
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class Labops(ABC):
    def __add__(self, __x: object) -> object:
        return Add(self, __x)
    def __mul__(self, __x: object) -> object:
        return Multiply(self, __x)

    @cache
    def is_divisible(self, by: int) -> bool:
        return self.get_remainder(by) == 0
    
    @abstractmethod
    def get_remainder(self, by: int) -> int:
        pass

class Operation(Labops):
    def __init__(self, a, b) -> None:
        self.a = a
        self.b = b
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.a}, {self.b})'


class Add(Operation):
    @cache
    def get_remainder(self, by: int) -> int:
        return (self.a.get_remainder(by) + self.b.get_remainder(by)) % by
    

class Multiply(Operation):
    @cache
    def get_remainder(self, by: int) -> int:
        return (self.a.get_remainder(by) * self.b.get_remainder(by)) % by

class Label(Labops, int):
    '''
    A class to mimic integer, but not really integer when it comes to multiplying and addition
    '''
    @cache
    def get_remainder(self, by: int) -> int:
        return self % by
    

class Monkey:
    def __init__(self, items: List, op: callable, test_div: callable) -> None:
        self.items = deque(items)
        self.op = op
        self.test_div = test_div
        self.inspection_count = 0
        
    def inspect_item(self, part1:bool = True):
        self.inspection_count += 1
        item = self.items.popleft()
        item = self.op(item)
        if part1:
            item = item // 3
        return self.test_div(item), item
    
    def __repr__(self) -> str:
        return repr(self.items)

    @classmethod
    def parse_monkey(cls, txt: str, part1: bool=True) -> object:
        monnum, start_items, operation, test, if_true, if_false = txt.strip().split('\n')
        start_text, item_text = start_items.split(':')
        IntLabel = int if part1 else Label
        items = [IntLabel(s) for s in item_text.split(', ')]
        oper, new, equal, old, sign, num = operation.strip().split(' ')
        if sign == '*':
            if num == 'old':
                f = lambda old: old*old
            else:
                f = lambda old: old*IntLabel(num)
        elif sign == '+':
            if num == 'old':
                f = lambda old: old+old
            else:
                f = lambda old: old+IntLabel(num)
        *_, by_num = test.strip().split(' ')
        *_, true_mon = if_true.strip().split(' ')
        *_, false_mon = if_false.strip().split(' ')
        if part1:
            test_f = lambda w: int(true_mon) if w % int(by_num) == 0 else int(false_mon)
        else:
            test_f = lambda w: int(true_mon) if w.is_divisible(int(by_num)) else int(false_mon)
        return cls(items, f, test_f)

def solve(monkeys: List[Monkey], rounds:int = 20, part1: bool=True) -> int:
    
    for round in range(rounds):
        m = 0
        while m < len(monkeys):
            while monkeys[m].items:
                monkey_to_receive, item = monkeys[m].inspect_item(part1)
                monkeys[monkey_to_receive].items.append(item)
            m+=1
            
                
                
    inspect_counts = sorted([monkey.inspection_count for monkey in monkeys], key=lambda x: -x)
    return inspect_counts[0] * inspect_counts[1]
                
@session.submit_result(level=1, tests=[({'inp': [
    '''Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3''',
    '''Monkey 1:
    Starting items: 54, 65, 75, 74
    Operation: new = old + 6
    Test: divisible by 19
        If true: throw to monkey 2
        If false: throw to monkey 0''',
    '''Monkey 2:
    Starting items: 79, 60, 97
    Operation: new = old * old
    Test: divisible by 13
        If true: throw to monkey 1
        If false: throw to monkey 3''',
    '''Monkey 3:
    Starting items: 74
    Operation: new = old + 3
    Test: divisible by 17
        If true: throw to monkey 0
        If false: throw to monkey 1'''
]}, 10605)])
def solve_part1(inp):
    monkeys = [Monkey.parse_monkey(monkey_text) for monkey_text in inp]
    return solve(monkeys)

@session.submit_result(level=2, tests=[({'inp': [
    '''Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3''',
    '''Monkey 1:
    Starting items: 54, 65, 75, 74
    Operation: new = old + 6
    Test: divisible by 19
        If true: throw to monkey 2
        If false: throw to monkey 0''',
    '''Monkey 2:
    Starting items: 79, 60, 97
    Operation: new = old * old
    Test: divisible by 13
        If true: throw to monkey 1
        If false: throw to monkey 3''',
    '''Monkey 3:
    Starting items: 74
    Operation: new = old + 3
    Test: divisible by 17
        If true: throw to monkey 0
        If false: throw to monkey 1'''
]}, 2713310158)])
def solve_part2(inp):
    monkeys = [Monkey.parse_monkey(monkey_text, part1=False) for monkey_text in inp]
    return solve(monkeys, 10000, part1=False)


if __name__ == '__main__':
    inp = session.read_input().split('\n\n')
    
    solve_part1(inp)
    
    solve_part2(inp)
