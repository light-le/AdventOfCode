'''
in:
2
4 2
1 2
1 3
1
3 1
2 3
2

out:
6 6 -1
-1 6
'''

class Node:
    def __init__(self, id):
        self.id = id
        self.children = []
        self._level = None
        self.linkeds = []
    
    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self, l):
        if self._level is None:
            self._level = l
            for node in self.linkeds:
                node.level = l + 1

    def __eq__(self, o):
        return self.id == o.id

class Graph:
    def __init__(self, start):
        self.start = start
        
    
def bfs(n, m, edges, s):
    # Write your code here
    root = Node(s)
    root.level = 0
    graph = Graph(root)
    
    all_nodes = {}
    
    for int1, int2 in edges:
        if int1 not in all_nodes:
            all_nodes[int1] = Node(int1)
        if int2 not in all_nodes:
            all_nodes[int2] = Node(int2)
        
        node1 = all_nodes[int1]
        node2 = all_nodes[int2]

        if node1.level is not None:
            node2.level = node1.level+1
        elif node2.level is not None:
            node1.level = node2.level+1
        else:
            node1.linkeds.append(node2)
            node2.linkeds.append(node1)
    
    node_list_no_root = [(id, node) for id, node in all_nodes.items() if id != s]
    sorted_nodes = sorted(node_list_no_root, key=lambda x: x[0])

