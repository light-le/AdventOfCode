from __future__ import annotations
from collections import deque
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class Node:
    '''Each node is actually a list'''
    def __init__(self, row: list[int]) -> None:
        self.row = deque(row)
        self.next = None
        self.prev = None
        
    def make_next_node(self) -> Node:
        return Node([(self.row[i] - self.row[i-1]) for i in range(1, len(self.row))])
    
    def is_homogenous(self) -> bool:
        '''all values are the same'''
        return len(self.row) > 1 and len(set(self.row)) == 1
    
    def add_next_number(self, number: int):
        self.row.append(number)
        
    def add_first_number(self, number: int):
        self.row.appendleft(number)
        
    def __str__(self) -> str:
        return ' '.join([str(s) for s in self.row])

class LinkedList:
    '''A list of lists, linked to each other'''
    def __init__(self, base: Node) -> None:
        self.base = base
        self.current_node = base
        
    def add_next_node(self) -> None:
        next_node = self.current_node.make_next_node()
        next_node.prev = self.current_node
        self.current_node.next = next_node
        self.current_node = next_node
        
    def add_last_number_to_node(self) -> None:
        number = self.current_node.row[-1]
        self.current_node = self.current_node.prev
        self.current_node.add_next_number(number + self.current_node.row[-1])
        
    def add_first_number_to_node(self) -> None:
        number = self.current_node.row[0]
        self.current_node = self.current_node.prev
        self.current_node.add_first_number(self.current_node.row[0] - number)
        
    def __str__(self) -> str:
        level = 0
        node = self.base
        printout = str(node)
        
        while node.next:
            level += 1
            node = node.next
            printout += '\n' + ' '*level + str(node)
        return printout

def find_next_number(line: list[int]) -> int:
    base_node = Node(line)
    sequence = LinkedList(base_node)
    
    sequence.add_next_node()
    
    while not sequence.current_node.is_homogenous():
        sequence.add_next_node()
    
    while sequence.current_node is not base_node:
        sequence.add_last_number_to_node()
    return base_node.row[-1]

@session.submit_result(level=1, tests=[({'inp': [
    '0 3 6 9 12 15',
    '1 3 6 10 15 21',
    '10 13 16 21 30 45'
]}, 114)])
def solve_part1(inp: list[str]) -> int:
    parsed_lines = [[int(s) for s in line.split()] for line in inp]
    return sum([find_next_number(line) for line in parsed_lines])
    

def find_prev_number(line: list[int]) -> int:
    base_node = Node(line)
    sequence = LinkedList(base_node)
    
    sequence.add_next_node()
    
    while not sequence.current_node.is_homogenous():
        sequence.add_next_node()
    
    while sequence.current_node is not base_node:
        sequence.add_first_number_to_node()
    return base_node.row[0]

@session.submit_result(level=2, tests=[({'inp': [
    '0 3 6 9 12 15',
    '1 3 6 10 15 21',
    '10 13 16 21 30 45'
]}, 2)])
def solve_part2(inp):
    parsed_lines = [[int(s) for s in line.split()] for line in inp]
    return sum([find_prev_number(line) for line in parsed_lines])


if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
