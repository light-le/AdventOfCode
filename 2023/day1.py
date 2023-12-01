
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

@session.submit_result(level=1, tests=[({'inp': [
    '1abc2',
    'pqr3stu8vwx',
    'a1b2c3d4e5f',
    'treb7uchet'
]}, 142)])
def solve_part1(inp: list[str]):
    total = 0
    for s in inp:
        for c in s:
            if c.isdigit():
                first_digit = c
                break
        for c in s[::-1]:
            if c.isdigit():
                last_digit = c
                break
        total += int(f'{first_digit}{last_digit}')
    return total

LETTER_DIGITS = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

@session.submit_result(level=2, tests=[({'inp': [
    'two1nine',
    'eightwothree',
    'abcfive2sevenxyz',
    'xtwone3four',
    '4nineeightseven2',
    'zoneight234',
    '7pqrstsixteen'
]}, 325), ({'inp': [
    '9eightone',
    'hczsqfour3nxm5seven4',
    '9twopjqkghmbone',
    'rhrfthv886vflthreeztvzs',
    'tlbtwo62five',
    'ninetwonine234nvtlzxzczx',
    '28sevenseven',
    '2sevensxszqdhjg2threexzjj3',
    '2fvq',
    '781dk97eight26',
    'plfrsjtbl6',
    'sixglj13'
]}, 91+44+91+83+25+94+27+23+22+76+66+63)])
def solve_part2(inp: list[str]):
    total = 0
    for line in inp:
        queue = []
        for letter, digit in LETTER_DIGITS.items():
            letter_ind = [i for i in range(len(line)) if line.startswith(letter, i)]
            queue.extend([(LETTER_DIGITS[letter], i) for i in letter_ind])
            
            digit_ind = [i for i in range(len(line)) if line[i] == digit]
            queue.extend([(digit, i) for i in digit_ind])
            
        first_digit = min(queue, key=lambda x: x[1])[0]
        last_digit = max(queue, key=lambda x: x[1])[0]
        
        total += int(f'{first_digit}{last_digit}')
    return total

if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
