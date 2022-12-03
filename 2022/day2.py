
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

item_scores = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

fight_result = {
    'X': {
        'A': 'D',
        'B': 'L',
        'C': 'W'
    },
    'Y': {
        'A': 'W',
        'B': 'D',
        'C': 'L'
    },
    'Z': {
        'A': 'L',
        'B': 'W',
        'C': 'D'
    },
}

point_result = {
    'W': 6,
    'D': 3,
    'L': 0
}

xyz_meaning = {
    'X': 'L', 'Y': 'D', 'Z': 'W'
}

fight_result2 = {
    'L': {
        'A': 'Z',
        'B': 'X',
        'C': 'Y'
    },
    'D': {
        'A': 'X',
        'B': 'Y',
        'C': 'Z'
    },
    'W': {
        'A': 'Y',
        'B': 'Z',
        'C': 'X'
    },
}

@session.submit_result(level=1, tests=[({'inp': [
    'A Y',
    'B X',
    'C Z',
]}, 15)])
def solve_part1(inp):
    total_points = 0
    for match in inp:
        opp, you = match.split()
        total_points += item_scores[you]
        total_points += point_result[fight_result[you][opp]]
    return total_points

@session.submit_result(level=2, tests=[({'inp': [
    'A Y',
    'B X',
    'C Z',
]}, 12)])
def solve_part2(inp):
    total_points = 0
    for round in inp:
        opp, res = round.split()
        you = fight_result2[xyz_meaning[res]][opp]
        total_points += item_scores[you]
        total_points += point_result[xyz_meaning[res]]
    return total_points


if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
