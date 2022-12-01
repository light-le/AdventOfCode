
from dataclasses import dataclass
from itertools import permutations
from subprocess import list2cmdline
from typing import List
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

@dataclass
class Node:
    filesystem: str
    size: int
    used: int
    avail: int
    used_percent: int
    
    @classmethod
    def parse_node(cls, data: str) -> object:
        file, size, used, avail, usedp = data.split()
        return cls(file,
                   int(size.replace('T', '')),
                   int(used.replace('T', '')),
                   int(avail.replace('T', '')),
                   int(usedp.replace('%', '')))
    

@session.submit_result(level=1)
def solve_part1(nodes: List[Node]):
    viables = 0
    for node1, node2 in permutations(nodes, 2):
        if node1.used > 0 and node1.used <= node2.avail:
            viables += 1
    return viables

@session.submit_result(level=2)
def solve_part2(inp):
    pass


if __name__ == '__main__':
    inp = [i for i in session.read_input().split('\n') if i]
    
    nodes = list(map(Node.parse_node, inp[2:]))
    
    solve_part1(nodes)
    
    solve_part2(inp)
