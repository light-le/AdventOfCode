
from typing import List
from functools import reduce
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

def count_outer_trees(w: int, h: int) -> int:
    return 2*(w+h) - 4

@session.submit_result(level=1, tests=[({'inp': [
    '30373',
    '25512',
    '65332',
    '33549',
    '35390',
]}, 21)])
def solve_part1(inp):
    outer_trees = count_outer_trees(len(inp), len(inp[0]))
    
    forest = [[int(tree) for tree in row] for row in inp]
    
    inner_visible = 0
    for r, row in enumerate(forest[1:-1], start=1):
        for c, tree in enumerate(row[1:-1], start=1):
            # assume invisible until find a path
            if any([
                all(left_tree < tree for left_tree in row[:c]),
                all(right_tree < tree for right_tree in row[c+1:]),
                all(top_tree < tree for top_tree in [col[c] for col in forest[:r]]),
                all(bottom_tree < tree for bottom_tree in [col[c] for col in forest[r+1:]])
            ]):
                inner_visible += 1
    return outer_trees + inner_visible

def nearest_visible_trees(h: int, trees: List[int]):
    visible_trees = list()
    while trees:
        visible_trees.append(trees.pop())
        if visible_trees[-1] >= h:
            break
    return len(visible_trees)

def scenic_score(*args):
    return reduce((lambda a, b: a*b), args)

@session.submit_result(level=2, tests=[({'inp': [
    '30373',
    '25512',
    '65332',
    '33549',
    '35390',
]}, 8)])
def solve_part2(inp):
    forest = [[int(tree) for tree in row] for row in inp]
    max_scenic_score = 0
    for r, row in enumerate(forest[1:-1], start=1):
        for c, tree in enumerate(row[1:-1], start=1):
            left_trees = nearest_visible_trees(tree, row[:c])
            right_trees = nearest_visible_trees(tree, row[c+1:][::-1])
            top_trees = nearest_visible_trees(tree, [col[c] for col in forest[:r]])
            bottom_trees = nearest_visible_trees(tree, [col[c] for col in forest[r+1:]][::-1])
            
            tree_score = scenic_score(left_trees, right_trees, top_trees, bottom_trees)
            max_scenic_score = max(max_scenic_score, tree_score)
    return max_scenic_score
            


if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
