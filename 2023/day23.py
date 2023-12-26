from __future__ import annotations
from dataclasses import dataclass, field
from utils import AdventSession, extract_year_day_from_path

@dataclass(frozen=True, eq=True)
class Point:
    row: int
    col: int

@dataclass
class Walker:
    pos: Point
    mapd: dict
    history: set = field(default_factory=set)
    steps_walked: int=0
    
    def next_walkable_poss(self) -> set[Point]:
        if self.mapd[self.pos] == '>':
            return {Point(self.pos.row, self.pos.col+1)} - self.history
        elif self.mapd[self.pos] == '<':
            return {Point(self.pos.row, self.pos.col-1)} - self.history
        elif self.mapd[self.pos] == '^':
            return {Point(self.pos.row-1, self.pos.col)} - self.history
        elif self.mapd[self.pos] == 'v':
            return {Point(self.pos.row+1, self.pos.col)} - self.history
        
        next_possibles = set()
        if self.mapd.get(Point(self.pos.row-1, self.pos.col), '#') not in ('#', 'v'):
            next_possibles.add(Point(self.pos.row-1, self.pos.col))
        if self.mapd.get(Point(self.pos.row+1, self.pos.col), '#') not in ('#', '^'):
            next_possibles.add(Point(self.pos.row+1, self.pos.col))
        if self.mapd.get(Point(self.pos.row, self.pos.col-1), '#') not in ('#', '>'):
            next_possibles.add(Point(self.pos.row, self.pos.col-1))
        if self.mapd.get(Point(self.pos.row, self.pos.col+1), '#') not in ('#', '<'):
            next_possibles.add(Point(self.pos.row, self.pos.col+1))
        return next_possibles - self.history
    
    def next_walkable_poss2(self) -> set[Point]:
        next_possibles = set()
        if self.mapd.get(Point(self.pos.row-1, self.pos.col), '#') != '#':
            next_possibles.add(Point(self.pos.row-1, self.pos.col))
        if self.mapd.get(Point(self.pos.row+1, self.pos.col), '#') != '#':
            next_possibles.add(Point(self.pos.row+1, self.pos.col))
        if self.mapd.get(Point(self.pos.row, self.pos.col-1), '#') != '#':
            next_possibles.add(Point(self.pos.row, self.pos.col-1))
        if self.mapd.get(Point(self.pos.row, self.pos.col+1), '#') != '#':
            next_possibles.add(Point(self.pos.row, self.pos.col+1))
        return next_possibles
    
    def walk(self, next_pos: Point) -> None:
        self.history.add(self.pos)
        self.steps_walked += 1
        self.pos = next_pos
        self.steps_since_last_node += 1
        
    def split(self) -> Walker:
        '''Basically make a copy of himself'''
        return Walker(pos=self.pos,
                      mapd=self.mapd.copy(),
                      history=self.history.copy(),
                      steps_walked=self.steps_walked)
            
session = AdventSession(**extract_year_day_from_path(__file__))

@session.submit_result(level=1, tests=[({'inp': [
    '#.#####################',
    '#.......#########...###',
    '#######.#########.#.###',
    '###.....#.>.>.###.#.###',
    '###v#####.#v#.###.#.###',
    '###.>...#.#.#.....#...#',
    '###v###.#.#.#########.#',
    '###...#.#.#.......#...#',
    '#####.#.#.#######.#.###',
    '#.....#.#.#.......#...#',
    '#.#####.#.#.#########v#',
    '#.#...#...#...###...>.#',
    '#.#.#v#######v###.###v#',
    '#...#.>.#...>.>.#.###.#',
    '#####v#.#.###v#.#.###.#',
    '#.....#...#...#.#.#...#',
    '#.#########.###.#.#.###',
    '#...###...#...#...#.###',
    '###.###.#.###v#####v###',
    '#...#...#.#.>.>.#.>.###',
    '#.###.###.#.###.#.#v###',
    '#.....###...###...#...#',
    '#####################.#'
]}, 94)])
def solve_part1(inp: list[str]) -> int:
    start = Point(0, inp[0].index('.'))
    stop = Point(len(inp)-1, inp[-1].index('.'))
    
    map = [list(line) for line in inp]
    # mapt = tuple([tuple(line) for line in inp])
    mapd = dict()
    for r, row in enumerate(map):
        mapd.update({Point(r, c): col for c, col in enumerate(row)})
        
    walker = Walker(pos=start, mapd=mapd)
    
    frontier = [walker]
    
    max_steps = 0
    
    while frontier:
        wal = frontier.pop()
        while wal.pos != stop:
            next_poss = wal.next_walkable_poss()
            if len(next_poss) == 1:
                [next_pos] = next_poss
                wal.walk(next_pos)
            elif len(next_poss) > 1:
                for next_pos in next_poss:
                    another_wal = wal.split()
                    another_wal.walk(next_pos)
                    frontier.append(another_wal)
                break
            elif len(next_poss) == 0:
                break # dead end
        
        if wal.pos == stop:
            max_steps = max(max_steps, wal.steps_walked)
    return max_steps

@dataclass(frozen=True)
class Path:
    from_node: Node
    weight: int
    to_node: Node
  
class Node:
    '''
    Basically an intersection
    '''
    def __init__(self, pos: Point) -> None:
        self.pos = pos
        self.paths = set()
        
    def __repr__(self) -> str:
        return f'{self.pos} {self.paths}'
    
    def __eq__(self, __value: object) -> bool:
        return self.pos == __value.pos
        
def find_next_steps(pos: Point, mapd: dict, history: set=None) -> set[Point]:
    history = history or set()
    next_possibles = set()
    if mapd.get(Point(pos.row-1, pos.col), '#') != '#':
        next_possibles.add(Point(pos.row-1, pos.col))
    if mapd.get(Point(pos.row+1, pos.col), '#') != '#':
        next_possibles.add(Point(pos.row+1, pos.col))
    if mapd.get(Point(pos.row, pos.col-1), '#') != '#':
        next_possibles.add(Point(pos.row, pos.col-1))
    if mapd.get(Point(pos.row, pos.col+1), '#') != '#':
        next_possibles.add(Point(pos.row, pos.col+1))
    return next_possibles - history

class Walker2:
    def __init__(self, current_node: Node, visited_node_points: set=None, steps_walked: int=0) -> None:
        self.current_node = current_node
        self.visited_node_points = visited_node_points or set()
        self.steps_walked = steps_walked
        
    def _split(self) -> Walker2:
        return Walker2(self.current_node, self.visited_node_points.copy(), self.steps_walked)
    
    def split_and_walk_to_next_new_node(self, inter_nodes: dict) -> list[Walker2]:
        walkers = list()
        self.visited_node_points.add(self.current_node.pos)
        for path in self.current_node.paths:
            if path.to_node in self.visited_node_points:
                continue
            new_walker = self._split()
            new_walker.steps_walked += path.weight
            new_walker.current_node = inter_nodes[path.to_node]
            walkers.append(new_walker)
        return walkers

@session.submit_result(level=2, tests=[({'inp': [
    '#.#####################',
    '#.......#########...###',
    '#######.#########.#.###',
    '###.....#.>.>.###.#.###',
    '###v#####.#v#.###.#.###',
    '###.>...#.#.#.....#...#',
    '###v###.#.#.#########.#',
    '###...#.#.#.......#...#',
    '#####.#.#.#######.#.###',
    '#.....#.#.#.......#...#',
    '#.#####.#.#.#########v#',
    '#.#...#...#...###...>.#',
    '#.#.#v#######v###.###v#',
    '#...#.>.#...>.>.#.###.#',
    '#####v#.#.###v#.#.###.#',
    '#.....#...#...#.#.#...#',
    '#.#########.###.#.#.###',
    '#...###...#...#...#.###',
    '###.###.#.###v#####v###',
    '#...#...#.#.>.>.#.>.###',
    '#.###.###.#.###.#.#v###',
    '#.....###...###...#...#',
    '#####################.#'
]}, 154)], wrong_answers={
    7272, # too high
    5838, # too low
    6364, # too low
    
})
def solve_part2(inp: list[str]) -> int:
    start = Point(0, inp[0].index('.'))
    stop = Point(len(inp)-1, inp[-1].index('.'))
    
    map = [list(line) for line in inp]
    mapd = dict()
    for r, row in enumerate(map):
        mapd.update({Point(r, c): col for c, col in enumerate(row)})
        
    intersection = dict()
    
    for point, value in mapd.items():
        if value == '#':
            continue
        surrounding_steps = find_next_steps(point, mapd)
        if len(surrounding_steps) > 2:
            intersection[point] = surrounding_steps
    
    intersection[start] = find_next_steps(start, mapd)
    print(f'{len(intersection)} intersections')
    
    inter_nodes = dict()
    node_before_stop = None
    final_steps = 0
    for inter_point, starting_points in intersection.items():
        node = Node(inter_point)
        inter_nodes[inter_point] = node
        for start_point in starting_points:
            steps = 1
            if start_point in intersection: # rare case that 2 intersections are next to each other
                node.paths.add(Path(inter_point, steps, start_point))
                continue
            history = {inter_point, start_point}
            
            next_points = find_next_steps(start_point, mapd, history)
            assert len(next_points) == 1, \
                f'Something wrong with these {next_points} as start_point {start_point} should have been in the intersections'

            next_point = next_points.pop()
            steps += 1
            while next_point not in intersection:
                history.add(next_point)
                next_points = find_next_steps(next_point, mapd, history)
                if next_points == set(): # dead-end, but not the stop
                    break
                next_point = next_points.pop()
                steps += 1
                if next_point == stop:
                    node.paths.add(Path(inter_point, steps, next_point))
                    node_before_stop = node
                    final_steps = steps
                    break
            if next_point in intersection:
                node.paths.add(Path(inter_point, steps, next_point))
    
    frontier = [Walker2(current_node=inter_nodes[start])]
    
    max_steps = 0
    while frontier:
        walker = frontier.pop()
        next_walkers = walker.split_and_walk_to_next_new_node(inter_nodes)
        
        for next_walker in next_walkers:
            if next_walker.current_node == node_before_stop:
                max_steps = max(max_steps, next_walker.steps_walked + final_steps)
            else:
                frontier.append(next_walker)
    return max_steps
        
        
    

if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
