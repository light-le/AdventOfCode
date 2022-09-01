
from collections import namedtuple
from typing import List
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

Disc = namedtuple('Disc', ['name', 'n_position', 't0_position'])

def parse_disc(txt: str) -> Disc:
    before, after = txt.split(';')
    disc, name, has, n_position, positions = before.split(' ')
    after_no_dot = after.replace('.', '')
    *_, t0_position = after_no_dot.split(' ')
    return Disc(name, int(n_position), int(t0_position))

def calculate_positions_at_fire(discs: List[Disc]) -> List[int]:
    positions_at_fire = []
    for t, disc in enumerate(discs):
        pos_at_fire = disc.n_position - (t+1)
        pos_at_fire = pos_at_fire + disc.n_position if pos_at_fire < 0 else pos_at_fire
        positions_at_fire.append(pos_at_fire)
        
    return positions_at_fire

def solve_part(discs: List[Disc]) -> int:
    pos_requirements = calculate_positions_at_fire(discs)
    
    product = 1
    t = 0
    for pos_req, disc in zip(pos_requirements, discs):
        disc_pos = (disc.t0_position + t) % disc.n_position
        while disc_pos != pos_req:
            t += product
            disc_pos = (disc_pos + product) % disc.n_position
        product *= disc.n_position
    return t

@session.submit_result(level=1, tests=[({'discs': [
    Disc(name='1', n_position=5, t0_position=4),
    Disc(name='2', n_position=2, t0_position=1)
]}, 5)])
def solve_part1(discs: List[Disc]):
    return solve_part(discs)

@session.submit_result(level=2)
def solve_part2(discs):
    return solve_part(discs)


if __name__ == '__main__':
    discs = [parse_disc(d) for d in session.read_input().split('\n') if d]
    
    solve_part1(discs)
    
    discs.append(Disc('n', n_position=11, t0_position=0))
    solve_part2(discs)
