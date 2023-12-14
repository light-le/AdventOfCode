from __future__ import annotations
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

@session.submit_result(level=1, tests=[({'inp': [
    'O....#....',
    'O.OO#....#',
    '.....##...',
    'OO.#O....O',
    '.O.....O#.',
    'O.#..O.#.#',
    '..O..#O..O',
    '.......O..',
    '#....###..',
    '#OO..#....'
]}, 136)])
def solve_part1(inp: list[str]):
    total_weights = 0
    for c in range(len(inp[0])):
        col = [row[c] for row in inp]
        
        o_i = [i for i, r in enumerate(col) if r == 'O']
        pound_i = [-1] + [i for i, r in enumerate(col) if r == '#'] + [len(inp)]
        
        for pi, p1 in enumerate(pound_i[:-1]):
            p2 = pound_i[pi+1]
            
            o_inbetween = [i for i in o_i if p1 < i < p2]
            
            tilted_oi = range(p1+1, p1+len(o_inbetween)+1)
            
            weights = sum([(len(inp) - ti) for ti in tilted_oi])
            
            total_weights += weights
    return total_weights
        
class BedRock:
    def __init__(self, map: list[str]) -> None:
        self.map = map
    def __hash__(self) -> int:
        return hash(tuple(self.map))
    def __eq__(self, __value: object) -> bool:
        return self.map == __value.map
     
    def __str__(self) -> str:
        return '\n'.join(self.map)
    
    def tilt_east(self) -> None:
        for r, row in enumerate(self.map):
            o_i = {c for c, char in enumerate(row) if char == 'O'}
            pound_i = [c for c, char in enumerate(row) if char == '#']
            
            new_o_i = set()
            for pi1, pi2 in zip([-1] + pound_i, pound_i + [len(row)]):
                o_inbetween = {i for i in o_i if pi1 < i < pi2}
                new_o_i |= set(range(pi2-len(o_inbetween), pi2))
            
            new_row = [None for _ in row]
            for c in range(len(row)):
                if c in pound_i:
                    new_row[c] = '#'
                elif c in new_o_i:
                    new_row[c] = 'O'
                else:
                    new_row[c] = '.'
            
            self.map[r] = ''.join(new_row)
            
    def tilt_west(self) -> None:
        self.map = [row[::-1] for row in self.map]
        self.tilt_east()
        self.map = [row[::-1] for row in self.map]
        
    def tilt_north(self) -> None:
        self.map = [''.join([row[i] for row in self.map]) for i in range(len(self.map[0]))]
        self.tilt_west()
        self.map = [''.join([row[i] for row in self.map]) for i in range(len(self.map[0]))]
        
    def tilt_south(self) -> None:
        self.map = [''.join([row[i] for row in self.map]) for i in range(len(self.map[0]))]
        self.tilt_east()
        self.map = [''.join([row[i] for row in self.map]) for i in range(len(self.map[0]))]
        
    def get_north_beam_weight(self) -> int:
        o_counts = [row.count('O') for row in self.map]
        o_weights = [(len(self.map) - r)*oc for r, oc in enumerate(o_counts)]
        return sum(o_weights)
    
    def spin_cycle(self) -> BedRock:
        new_bedrock = BedRock(self.map.copy())
        new_bedrock.tilt_north()
        new_bedrock.tilt_west()
        new_bedrock.tilt_south()
        new_bedrock.tilt_east()
        return new_bedrock


@session.submit_result(level=2, tests=[({'inp': [
    'O....#....',
    'O.OO#....#',
    '.....##...',
    'OO.#O....O',
    '.O.....O#.',
    'O.#..O.#.#',
    '..O..#O..O',
    '.......O..',
    '#....###..',
    '#OO..#....'
]}, 64)], print_only=True)
def solve_part2(inp: list[str]):
    br = BedRock(inp)
    
    cyclepedia = dict()
    
    for c in range(10**9):
        br = br.spin_cycle()
        c += 1
        
        print(f'Finished spinning cycle {c}')
        if br in cyclepedia:
            print(f'found repeated state after cycle {c}. This has happened before at cycle and weight {cyclepedia[br]}')
            break
        cyclepedia[br] = (c, br.get_north_beam_weight())
        
    cycles_left = 10**9 - c
    past_cycles, past_weight = cyclepedia[br]
    repeated_cycles = c - past_cycles
    
    remaining_cycles = cycles_left % repeated_cycles
    
    cycle_to_look_for = past_cycles + remaining_cycles
    
    for cycle, weight in cyclepedia.values():
        if cycle == cycle_to_look_for:
            return weight

if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
