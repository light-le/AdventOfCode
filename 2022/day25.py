
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

def symbol_to_num(s: str) -> int:
    if s == '-':
        return -1
    elif s == '=':
        return -2
    else:
        return int(s)
    
def symbol_decrement(s: str) -> str:
    '''Make sure s is not ='''
    if s == '0':
        return '-'
    elif s == '-':
        return '='
    else:
        return str(int(s) - 1)

def snafu_to_number_converter(sf: str) -> int:
    length = len(sf)
    number = 0
    for c, char in enumerate(sf, start=1):
        number += 5**(length-c)*symbol_to_num(char)
    return number
    
def number_to_snafu_converter(num: int) -> str:
    length = 1
    while snafu_to_number_converter('2'*length) < num:
        length += 1
    guess_snafu = ['2' for _ in range(length)]
    i = 0
    while snafu_to_number_converter(''.join(guess_snafu)) != num:
        try_snafu = guess_snafu.copy()
        if i == 0 and try_snafu[i] == '1':
            i+=1
        elif try_snafu[i] != '=':
            try_snafu[i] = symbol_decrement(try_snafu[i])
        else:
            i += 1
        try_num = snafu_to_number_converter(''.join(try_snafu))
        if try_num > num:
            guess_snafu = try_snafu.copy()
        elif try_num == num:
            return ''.join(try_snafu)
        else:
            i+=1
    return ''.join(guess_snafu)
        
@session.submit_result(level=1, tests=[({'inp': [
    '1=-0-2',
    '12111',
    '2=0=',
    '21',
    '2=01',
    '111',
    '20012',
    '112',
    '1=-1=',
    '1-12',
    '12',
    '1=',
    '122'
]}, '2=-1=0')])
def solve_part1(inp):
    total_fuel = sum([snafu_to_number_converter(line) for line in inp])
    return number_to_snafu_converter(total_fuel)

@session.submit_result(level=2)
def solve_part2(inp):
    pass


if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
