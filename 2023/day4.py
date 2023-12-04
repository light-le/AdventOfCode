
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

@session.submit_result(level=1, tests=[({'inp': [
    'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
    'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
    'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
    'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
    'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
    'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'
]}, 13)])
def solve_part1(inp: list[str]):
    total_points = 0
    for line in inp:
        card_number, content = line.split(': ')
        winning, actual = content.split(' | ')
        winning_numbers = {int(s) for s in winning.split()}
        actual_list = actual.split()
        actual_numbers = {int(s) for s in actual_list}
        assert len(actual_numbers) == len(actual_list), f'duplicate at {line}'
        
        commons = winning_numbers & actual_numbers
        if len(commons) > 0:
            total_points += 2**(len(commons)-1)
    return total_points

@session.submit_result(level=2, tests=[({'inp': [
    'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
    'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
    'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
    'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
    'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
    'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'
]}, 30)])
def solve_part2(inp: list[str]):
    total_copies = {i+1: 1 for i in range(len(inp))}
    for c, line in enumerate(inp, start=1):
        card_number, content = line.split(': ')
        winning, actual = content.split(' | ')
        winning_numbers = {int(s) for s in winning.split()}
        actual_list = actual.split()
        actual_numbers = {int(s) for s in actual_list}

        commons = winning_numbers & actual_numbers
        wins = len(commons)
        if wins > 0:
            for card_no in range(c+1, c+wins+1):
                total_copies[card_no] += total_copies[c]
    return sum(total_copies.values())

if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
