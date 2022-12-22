from typing import List
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class Number():
    id = 0
    all_numbers = dict()
    def __init__(self, n) -> None:
        self.value = int(n)
        self.id = self.__class__.id
        self.__class__.all_numbers[id] = self
        self.__class__.id += 1
        
    def __add__(self, __o) -> int:
        return self.value + __o.value
        
    def __eq__(self, __o) -> bool:
        return self.value == __o.value
    
    def __repr__(self) -> str:
        return f'{self.value}'
    
    def __str__(self) -> str:
        return f'ID {self.id} value {self.value}'

class Node:
    def __init__(self, value, id) -> None:
        self.value = value
        self.next = None
        self.prev = None
        self.id = id

    def connect(self, node: object) -> None:
        self.next = node
        node.prev = self
        
class CircularLinkedList:
    def __init__(self, list: List) -> None:
        node = None
        id = 0
        for item in list:
            next_node = Node(item, id)
            if node:
                node.connect(next_node)
            else:
                self.head = next_node
            id += 1
            node = next_node
            
            if next_node.value == 0:
                self.zero_node = next_node
        node.connect(self.head)
        self.length = len(list)
        
    def aslist(self):
        node = self.head
        id = 0
        l = list()
        while id < self.length:
            l.append(node.value)
            id += 1
            node = node.next
        return l
    
    def __repr__(self) -> str:
        return str(self.aslist())
        
    def __len__(self) -> int:
        return self.length
    
    def find_node_at(self, id: int = 0):
        assert id < self.length, f'Not possible'
        node = self.head
        while node.id != id:
            node = node.next
        return node
    
    def transfer_node_by_value(self, node: Node):
        value = node.value
        if value == 0:
            return None
        
        if abs(value) > 1e6:
            value = value % (self.length-1)
        node.prev.connect(node.next)
        if value > 0:
            next_node = node.next
            value -= 1
            while value > 0:
                next_node = next_node.next
                value -= 1
            next2_node = next_node.next
            next_node.connect(node)
            node.connect(next2_node)
        elif value < 0:
            prev_node = node.prev
            value += 1
            while value < 0:
                prev_node = prev_node.prev
                value += 1
            prev2_node = prev_node.prev
            prev2_node.connect(node)
            node.connect(prev_node)
            
    def get_grove_coordinates(self) -> int:
        node = self.zero_node
        total = 0
        for i in range(1, 3001):
            node = node.next
            if i % 1000 == 0:
                total += node.value
        return total

@session.submit_result(level=1, tests=[({'inp': [
    '1',
    '2',
    '-3',
    '3',
    '-2',
    '0',
    '4',
]}, 3)])
def solve_part1(inp):
    cirll = CircularLinkedList([int(line) for line in inp])
    
    for id in range(len(cirll)):
        node = cirll.find_node_at(id)
        cirll.transfer_node_by_value(node)
    return cirll.get_grove_coordinates()
        
def solver(inp):
    Number.id = 0
    Number.all_numbers = dict()
    
    numbers = [Number(int(n)*811589153) for n in inp]
    for mix in range(10):
        for id in range(len(numbers)):
            for n in range(len(numbers)):
                if numbers[n].id == id:
                    numval = numbers[n].value
                    if numval == 0:
                        break
                    nindex = n + numval
                    if nindex >= 0:
                        new_index = nindex%len(numbers)
                    else:
                        new_index = len(numbers) - (-nindex % len(numbers))
                    add_index = 1 if numval > 0 else 0 
                    if new_index <= n:
                        numbers = numbers[:new_index+add_index] + [numbers[n]] + numbers[new_index+add_index:n] + numbers[n+1:]
                    else:
                        numbers = numbers[:n] + numbers[n+1:new_index+add_index] + [numbers[n]] + numbers[new_index+add_index:]
                    break
            
    zero_i = [n.value for n in numbers].index(0)
    
    return sum([numbers[(zero_i+i)%len(numbers)].value for i in [1000, 2000, 3000]])
                
                    

@session.submit_result(level=2, tests=[({'inp': [
    '1',
    '2',
    '-3',
    '3',
    '-2',
    '0',
    '4',
]}, 1623178306)])
def solve_part2(inp):
    cirll = CircularLinkedList([int(line)*811589153 for line in inp])
    
    for mixing in range(10):
        for id in range(len(cirll)):
            node = cirll.find_node_at(id)
            cirll.transfer_node_by_value(node)
    return cirll.get_grove_coordinates()

if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
