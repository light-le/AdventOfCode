
from collections import deque
from math import ceil
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

@session.submit_result(level=1, tests=[({'inp': '5'}, 3)])
def solve_part1(inp):
    elves = list(range(1, int(inp)+1))
    while len(elves) > 1:
        if len(elves) % 2 == 0:
            elves = elves[::2]
        else:
            elves = elves[2::2]
    [winner] = elves
    return winner

@session.submit_result(level=2, tests=[({'inp': '5'}, 2), ({'inp': '10'}, 1)])
def solve_part2(inp):
    elves = list(range(1, int(inp)+1))
    elve_queue = deque(elves[ceil(len(elves)/2):] + elves[:ceil(len(elves)/2)])
    i = int(inp) % 2
    
    while len(elve_queue) > 1:
        i+=1
        if i % 2 == 1:
            elve_queue.popleft()
        else:
            elve_queue.pop()
        
        elve_queue.append(elve_queue.popleft())

    winner = elve_queue.pop()
    return winner
         
    

if __name__ == '__main__':
    inp = session.read_input().strip()
    
    solve_part1(inp)
    
    solve_part2(inp)
