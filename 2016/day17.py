
from collections import deque, namedtuple
from enum import Enum
from hashlib import md5
import queue
from typing import Callable, List
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

Point = namedtuple("Point", ['x', 'y'])

md5hash = lambda t: md5(t.encode()).hexdigest()

class Directions(Enum):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'

OPEN_CODES = 'bcdef'


class Player:
    def __init__(self, passcode: str, coor: Point=Point(0, 0), past_dirs: str='') -> None:
        self.coor = coor
        self.passcode = passcode
        self.past_directions = past_dirs
        
    def derive_possible_moves(self) -> List[Directions]:
        hash = md5hash(self.passcode+self.past_directions)[:4]
        possible_moves = []
        if hash[0] in OPEN_CODES and self.coor.y > 0:
            possible_moves.append(Player(coor=Point(self.coor.x, self.coor.y-1),
                                         passcode=self.passcode,
                                         past_dirs=self.past_directions+Directions.UP.value))
        if hash[1] in OPEN_CODES and self.coor.y < 3:
            possible_moves.append(Player(coor=Point(self.coor.x, self.coor.y+1),
                                         passcode=self.passcode,
                                         past_dirs=self.past_directions+Directions.DOWN.value))
        if hash[2] in OPEN_CODES and self.coor.x > 0:
            possible_moves.append(Player(coor=Point(self.coor.x-1, self.coor.y),
                                         passcode=self.passcode,
                                         past_dirs=self.past_directions+Directions.LEFT.value))
        if hash[3] in OPEN_CODES and self.coor.x < 3:
            possible_moves.append(Player(coor=Point(self.coor.x+1, self.coor.y),
                                         passcode=self.passcode,
                                         past_dirs=self.past_directions+Directions.RIGHT.value))
        return possible_moves
        
@session.submit_result(level=1, tests=[
    ({'inp': 'ihgpwlah'}, 'DDRRRD'),
    ({'inp': 'kglvqrro'}, 'DDUDRLRRUDRD'),
    ({'inp': 'ulqzkmiv'}, 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'),
])
def solve_part1(inp):
    player = Player(passcode=inp)
    frontier = deque([player])
    
    while frontier:
        if queue:
            player = frontier.popleft()
        else:
            player = frontier.pop()

        if player.coor == Point(3, 3):
            return player.past_directions
        possible_players = player.derive_possible_moves()
        frontier.extend(possible_players)
        frontier = deque(sorted(frontier, key=lambda p: (3-p.coor.x)+(3-p.coor.y)+len(p.past_directions)))

@session.submit_result(level=2, tests=[
    ({'inp': 'ihgpwlah'}, 370),
    ({'inp': 'kglvqrro'}, 492),
    ({'inp': 'ulqzkmiv'}, 830),
])
def solve_part2(inp):
    player = Player(passcode=inp)
    frontier = deque([player])
    vault_players = list()
    
    while frontier:
        player = frontier.popleft()
        possible_players = player.derive_possible_moves()
        
        vault_players.extend([player for player in possible_players if player.coor == Point(3, 3)])  
        frontier.extend([player for player in possible_players if player.coor != Point(3, 3)])
    vault_players = sorted(vault_players, key=lambda p: len(p.past_directions))
    longest_player = vault_players.pop()

    return len(longest_player.past_directions)

if __name__ == '__main__':
    inp = session.read_input().strip()
    
    solve_part1(inp)
    
    solve_part2(inp)
