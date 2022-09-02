
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

def mirror(bin: str) -> str:
    bin_rev = bin[::-1]
    bin_01_switch = bin_rev.replace('0', '2').replace('1', '0').replace('2', '1')
    return bin + '0' + bin_01_switch

def checksum(txt: str) -> str:
    pairs = [txt[c:c+2] for c in range(0, len(txt), 2)]
    news = ''
    for pair in pairs:
        if pair == '00' or pair == '11':
            news += '1'
        elif pair == '01' or pair == '10':
            news += '0'
        else:
            raise Exception(f'Invalid pair {pair}')
    return news

def solve_part(inp: str, length: int):
    while len(inp) < length:
        inp = mirror(inp)
    disk = inp[:length]
    
    cs = checksum(disk)
    while len(cs) % 2 == 0:
        cs = checksum(cs)
    return cs


@session.submit_result(level=1, tests=[({'inp': '10000', 'length': 20}, '01100')])
def solve_part1(inp, length=272):
    return solve_part(inp, length)

@session.submit_result(level=2)
def solve_part2(inp):
    return solve_part(inp, length=35651584)


if __name__ == '__main__':
    inp = session.read_input().strip()
    
    solve_part1(inp)
    
    solve_part2(inp)
