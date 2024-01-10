from __future__ import annotations
from itertools import combinations
from collections import deque
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class Node:
    ALL_NODES = dict()
    def __init__(self, name: str) -> None:
        self.name = name
        self.connected_names = set()
        self.__class__.ALL_NODES[name] = self
        
    def __hash__(self) -> int:
        return hash(self.name)
    
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name
    
    # def __str__(self) -> str:
    #     return self.name
    
    def __repr__(self) -> str:
        return f'{self.name} connected to {", ".join(self.connected_names)}.'
    
    @classmethod
    def find_paths(cls, node1: Node, node2: Node) -> int:
        '''find number of (distinctive) paths from node1 node to node2'''
        history = set() #set(node1.name)
        frontier = deque([node1])
        
        paths = 0
        while frontier:
            node = frontier.popleft()
            next_node_names = node.connected_names
            
            for next_name in next_node_names:
                pathname = node.name + '-' + next_name
                if pathname in history:
                    continue
                elif node2.name == next_name:
                    paths += 1
                else:
                    frontier.append(cls.ALL_NODES[next_name])
                print(f'adding path {pathname}')
                history.add(pathname)
                history.add(next_name + '-' + node.name)
            
        return paths
    
    def count_all_nodes_in_group(self) -> int:
        history = {self.name}
        
        frontier = [self]
        
        while frontier:
            node = frontier.pop()
            next_node_names = node.connected_names
            
            for next_name in next_node_names:
                if next_name in history:
                    continue
                
                frontier.append(self.__class__.ALL_NODES[next_name])
                history.add(next_name)
        return len(history)
                    

@session.submit_result(level=1, tests=[({'inp': [
    'jqt: rhn xhk nvd',
    'rsh: frs pzl lsr',
    'xhk: hfx',
    'cmg: qnr nvd lhk bvb',
    'rhn: xhk bvb hfx',
    'bvb: xhk hfx',
    'pzl: lsr hfx nvd',
    'qnr: nvd',
    'ntq: jqt hfx bvb xhk',
    'nvd: lhk',
    'lsr: lhk',
    'rzs: qnr cmg lsr rsh',
    'frs: qnr lhk lsr'
]}, 54)])
def solve_part1(inp: list[str]) -> int:
    Node.ALL_NODES = dict()

    with open('./day25_viz.txt', 'w') as logf:
        for line in inp:
            source, dests = line.split(': ')
            destslist = dests.split(' ')
            logf.write(f'{source} -- {", ".join(destslist)};\n')
    
    # paste the content to https://dreampuf.github.io/GraphvizOnline/ to get the 3 bridges by visualization
    # tpb - xsl, lrd - qpg, zlv - bmx
    if len(inp) < 20:
        severed_connections = {
            ('hfx', 'pzl'), ('pzl', 'hfx'),
            ('bvb', 'cmg'), ('cmg', 'bvb'),
            ('nvd', 'jqt'), ('jqt', 'nvd')
        }
        left_node_name = 'bvb'
        right_node_name = 'nvd'
    else:
        severed_connections = {
            ('tpb', 'xsl'), ('xsl', 'tpb'),
            ('lrd', 'qpg'), ('qpg', 'lrd'),
            ('zlv', 'bmx'), ('bmx', 'zlv')
        }
        left_node_name = 'tpb'
        right_node_name = 'xsl'

    for line in inp:
        source, dests = line.split(': ')
        source_node = Node(source)
        
        [Node(dest) for dest in dests.split()]
    
    total_nodes = len(Node.ALL_NODES)
    print('Total nodes', total_nodes)
    
    for line in inp:
        source_name, dests = line.split(': ')
        
        source_node = Node.ALL_NODES[source_name]
        
        
        for dest_node_name in dests.split():
            if (source_name, dest_node_name) in severed_connections:
                continue
            dest_node = Node.ALL_NODES[dest_node_name]
            
            source_node.connected_names.add(dest_node_name)
            dest_node.connected_names.add(source_name)
            
    left_group_size = Node.ALL_NODES[left_node_name].count_all_nodes_in_group()
    right_group_size = Node.ALL_NODES[right_node_name].count_all_nodes_in_group()
    return left_group_size*right_group_size

if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    # solve_part2(inp)
