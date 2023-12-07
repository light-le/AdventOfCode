# from functools import cache
from functools import reduce
from math import sqrt, ceil, floor
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

def distance_at_charge_time(t: int, total_time: int) -> int:
    return t*(total_time-t)

def calculate_possible_distances(time: int) -> list[int]:
    return [distance_at_charge_time(t, total_time=time) for t in range(time+1)]

@session.submit_result(level=1, tests=[({'inp': [
    'Time:      7  15   30',
    'Distance:  9  40  200'
]}, 288)])
def solve_part1(inp: list[str]):
    time_line, dist_line = inp
    times = [int(s) for s in time_line.replace('Time:', '').split()]
    record_distances = [int(s) for s in dist_line.replace('Distance:', '').split()]
    
    possible_distances = [calculate_possible_distances(time) for time in times]
    
    better_distance_count = [len(
        [d for d in poss_dist if d > record_dist]) for poss_dist, record_dist in zip(possible_distances, record_distances)
    ]
    return reduce(lambda a, b: a*b, better_distance_count)

@session.submit_result(level=2, tests=[({'inp': [
    'Time:      7  15   30',
    'Distance:  9  40  200'
]}, 71503)])
def solve_part2(inp: list[str]):
    time_line, dist_line = inp
    time = int(time_line.replace('Time:', '').replace(' ', ''))
    record_distance = int(dist_line.replace('Distance:', '').replace(' ', ''))
    
    # solve for t in -t**2 + time*t - record_distance = 0
    delta = time**2 - 4*(-1)*(-record_distance)
    small_t = (-time - sqrt(delta))/(-2)
    big_t = (-time + sqrt(delta))/(-2)
    
    return int(max(big_t, small_t)) - int(min(big_t, small_t))

if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
