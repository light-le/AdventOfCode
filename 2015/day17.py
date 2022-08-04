from itertools import combinations, accumulate

from utils import AdventSession, extract_year_day_from_path

def determine_max_min(acc):
    for a, ac in enumerate(acc):
        if ac > 150:
            return a+1

def possible_container_combinations(scs):
    maximum_containers = determine_max_min(accumulate(scs))
    minimum_containers = determine_max_min(accumulate(scs[::-1]))

    combs = [combinations(scs, r) for r in range(minimum_containers, maximum_containers+1)]
    
    possible_combinations = []
    for comb in combs:
        rcomb = [rc for rc in comb if sum(rc) == 150]
        possible_combinations.extend(rcomb)
        
    return possible_combinations

def solve_part2(possible_combinations):
    minimum_length = min(len(comb) for comb in possible_combinations)
    return len([mincomp for mincomp in possible_combinations if len(mincomp) == minimum_length])

if __name__ == '__main__':
    session = AdventSession(**extract_year_day_from_path(__file__))
    
    containers = [int(c) for c in session.read_input().split('\n') if c]
    
    sortainers = sorted(containers)
    
    possible_containers = possible_container_combinations(sortainers)

    part1_answer = len(possible_containers)
    print(part1_answer)
    session.post_answer(part1_answer, level=1)
    
    part2_answer = solve_part2(possible_containers)
    print(part2_answer)
    session.post_answer(part2_answer, level=2)