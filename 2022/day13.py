from typing import List
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

def compare_lists(l1: List, l2: List) -> bool:
    for i1, i2 in zip(l1, l2):
        if isinstance(i1, int) and isinstance(i2, int):
            if i1 < i2:
                return True
            elif i1 > i2:
                return False
            else:
                continue
        elif isinstance(i1, list) and isinstance(i2, list):
            result = compare_lists(i1, i2)
        elif isinstance(i1, list) and isinstance(i2, int):
            result = compare_lists(i1, [i2])
        elif isinstance(i1, int) and isinstance(i2, list):
            result = compare_lists([i1], i2)
        else:
            raise Exception(f'Not possible. i1 {i1}. i2 {i2}')
        
        if isinstance(result, bool):
            return result

    if len(l1) < len(l2):
        return True
    elif len(l1) > len(l2):
        return False
        
    
    
@session.submit_result(level=1, tests=[({'inp': [
    '[1,1,3,1,1]',
    '[1,1,5,1,1]',
    '',
    '[[1],[2,3,4]]',
    '[[1],4]',
    '',
    '[9]',
    '[[8,7,6]]',
    '',
    '[[4,4],4,4]',
    '[[4,4],4,4,4]',
    '',
    '[7,7,7,7]',
    '[7,7,7]',
    '',
    '[]',
    '[3]',
    '',
    '[[[]]]',
    '[[]]',
    '',
    '[1,[2,[3,[4,[5,6,7]]]],8,9]',
    '[1,[2,[3,[4,[5,6,0]]]],8,9]',
]}, 13)])
def solve_part1(inp):
    index = (len(inp)+1)//3
    total = 0
    while inp:
        second = eval(inp.pop())
        first = eval(inp.pop())
        
        right_order = compare_lists(first, second)
        print(right_order)
        if right_order:
            print(index, first, second)
            total += index
        
        index -= 1
        if inp:
            inp.pop()
    return total

class Package(list):
    def __lt__(self, __o: object) -> bool:
        return compare_lists(self, __o)


@session.submit_result(level=2, tests=[({'inp': [
    '[1,1,3,1,1]',
    '[1,1,5,1,1]',
    '',
    '[[1],[2,3,4]]',
    '[[1],4]',
    '',
    '[9]',
    '[[8,7,6]]',
    '',
    '[[4,4],4,4]',
    '[[4,4],4,4,4]',
    '',
    '[7,7,7,7]',
    '[7,7,7]',
    '',
    '[]',
    '[3]',
    '',
    '[[[]]]',
    '[[]]',
    '',
    '[1,[2,[3,[4,[5,6,7]]]],8,9]',
    '[1,[2,[3,[4,[5,6,0]]]],8,9]',
]}, 140)])
def solve_part2(inp):
    divider2 = Package([[2]])
    divider6 = Package([[6]])
    
    all_lists = [divider2, divider6]
    for line in inp:
        if line:
            all_lists.append(Package(eval(line)))
            
    sorted_list = sorted(all_lists)
    return (sorted_list.index(divider2)+1)*(sorted_list.index(divider6)+1)
    


if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp.copy())
    
    solve_part2(inp.copy())
