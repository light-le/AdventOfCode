
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

@session.submit_result(level=1, tests=[
    ({'inp': 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'}, 7),
    ({'inp': 'bvwbjplbgvbhsrlpgdmjqwftvncz'}, 5),
    ({'inp': 'nppdvjthqldpwncqszvftbrmjlhg'}, 6),
    ({'inp': 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'}, 10),
    ({'inp': 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'}, 11),
])
def solve_part1(inp):
    
    for c in range(len(inp) - 4):
        if len(set(inp[c:c+4])) == 4:
            return c+4

@session.submit_result(level=2, tests=[
    ({'inp': 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'}, 19),
    ({'inp': 'bvwbjplbgvbhsrlpgdmjqwftvncz'}, 23),
    ({'inp': 'nppdvjthqldpwncqszvftbrmjlhg'}, 23),
    ({'inp': 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'}, 29),
    ({'inp': 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'}, 26),
])
def solve_part2(inp):
    for c in range(len(inp) - 14):
        if len(set(inp[c:c+14])) == 14:
            return c+14
    


if __name__ == '__main__':
    inp = session.read_input()
    
    solve_part1(inp)
    
    solve_part2(inp)
