
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class TrapMap:
    map = list()
    def __init__(self, line: str) -> None:
        self.line = line
        self.map.append(line)
    
    def derive_next_line(self) -> object:
        c = 0
        next_line = ''
        while c < len(self.line):
            if c == 0:
                if self.line[:2] == '^^' or self.line[:2] == '.^':
                    next_line += '^'
                else:
                    next_line += '.'
            elif c == len(self.line) - 1:
                if self.line[-2:] == '^^' or self.line[-2:] == '^.':
                    next_line += '^'
                else:
                    next_line += '.'
            else:
                oldline = self.line[c-1:c+2]
                if oldline in ['^^.', '^..', '..^', '.^^']:
                    next_line += '^'
                else:
                    next_line += '.'
            c+=1
        return TrapMap(next_line)
    
    @property
    def safe_tiles(self) -> int:
        return self.line.count('.')

def solve_part(inp: str, times: int):
    trap = TrapMap(inp)
    safe_tiles = trap.safe_tiles
    for _ in range(times-1):
        trap = trap.derive_next_line()
        safe_tiles += trap.safe_tiles
    return safe_tiles

@session.submit_result(level=1, tests=[
    ({'inp': '..^^.', 'times': 3}, 6),
    ({'inp': '.^^.^.^^^^', 'times': 10}, 38),
])
def solve_part1(inp, times=40):
    return solve_part(inp, times)

@session.submit_result(level=2)
def solve_part2(inp):
    return solve_part(inp, times=400000)


if __name__ == '__main__':
    inp = session.read_input().strip()
    
    solve_part1(inp)
    
    solve_part2(inp)
