from statistics import median
from functools import reduce
error_scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
complete_scores = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

open_close = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}

close_open = {v: k for k,v in open_close.items()}

def calculate_error_score(code):
    opens = []
    for c in code:
        if c in ['(', '[', '{', '<']:
            opens.append(c)
        else: # c is a close
            if not opens: # there's no preceding open
                return error_scores[c]
            latest_open = opens.pop()
            if open_close[c] != latest_open:
                return error_scores[c]
    return 0

def part1_solution(codes):
    return sum([calculate_error_score(code) for code in codes])


def calculate_complete_score(code):
    opens = []
    for c in code:
        if c in ['(', '[', '{', '<']:
            opens.append(c)
        else: # c is a close
            if not opens: # there's no preceding open
                return None
            latest_open = opens.pop()
            if open_close[c] != latest_open:
                return None
    auto_complete = [close_open[op] for op in opens[::-1]]
    auto_score = [complete_scores[at] for at in auto_complete]
    return reduce((lambda a,b:a*5+b), auto_score)

def part2_solution(codes):
    return median([score for score in [calculate_complete_score(code) for code in codes] if score])

if __name__ == "__main__":
    with open('2021/day10.txt', 'r') as f:
        codes = f.read().rsplit()
    print(part1_solution(codes))
    print(part2_solution(codes))