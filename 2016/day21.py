
from collections import deque
from itertools import permutations
from typing import List
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class Scrambler:
    def __init__(self, password) -> None:
        self.password = list(password)
        
    def swap_positions(self, x: int, y: int):
        self.password[x], self.password[y] = self.password[y], self.password[x]
        
    def swap_letters(self, lx: str, ly: str):
        x = self.password.index(lx)
        y = self.password.index(ly)
        self.swap_positions(x, y)
        
    def rotate(self, r: int):
        password = deque(self.password)
        password.rotate(r)
        self.password = list(password)
        
    def rotate_based_on(self, lx: str):
        x = self.password.index(lx)
        r = 1 + x if x < 4 else 2 + x
        self.rotate(r)
        
    def unrotate_based_on(self, lx: str):
        self.rotate(-1)
        guess_index = 0
        
        while guess_index != self.password.index(lx):
            self.rotate(-1)
            guess_index += 1
            if guess_index == 4:
                self.rotate(-1)
            
    
    def reverse_positions(self, x: int, y: int):
        self.password = self.password[:x] + self.password[x:y+1][::-1] + self.password[y+1:]
        
    def move_positions(self, x: int, y:int):
        removed = self.password.pop(x)
        self.password = self.password[:y]+[removed]+self.password[y:]
        
    def parse_commands(self, cmd: str):
        cmdsplit = cmd.split(' ')
        if cmd.startswith('swap position'):
            swap, position, x, with_, position2, y = cmdsplit
            self.swap_positions(int(x), int(y))
        elif cmd.startswith('swap letter'):
            swap, letter, lx, with_, letter2, ly = cmdsplit
            self.swap_letters(lx, ly)
        elif cmd.startswith('rotate left'):
            rotate, left, x, steps = cmdsplit
            self.rotate(-int(x))
        elif cmd.startswith('rotate right'):
            rotate, right, x, steps = cmdsplit
            self.rotate(int(x))
        elif cmd.startswith('rotate based'):
            rotate, based, on, position, of, letter, lx = cmdsplit
            self.rotate_based_on(lx)
        elif cmd.startswith('reverse'):
            reverse, positions, x, through, y = cmdsplit
            self.reverse_positions(int(x), int(y))
        elif cmd.startswith('move'):
            move, position, x, to, position2, y = cmdsplit
            self.move_positions(int(x), int(y))
        else:
            raise Exception(f'Invalid command {cmd}')
        
        
    def parse_unscrambled_commands(self, cmd):
        cmdsplit = cmd.split(' ')
        if cmd.startswith('swap position'):
            swap, position, x, with_, position2, y = cmdsplit
            self.swap_positions(int(x), int(y))
        elif cmd.startswith('swap letter'):
            swap, letter, lx, with_, letter2, ly = cmdsplit
            self.swap_letters(lx, ly)
        elif cmd.startswith('rotate left'):
            rotate, left, x, steps = cmdsplit
            self.rotate(int(x))
        elif cmd.startswith('rotate right'):
            rotate, right, x, steps = cmdsplit
            self.rotate(-int(x))
        elif cmd.startswith('rotate based'):
            rotate, based, on, position, of, letter, lx = cmdsplit
            self.unrotate_based_on(lx)
        elif cmd.startswith('reverse'):
            reverse, positions, x, through, y = cmdsplit
            self.reverse_positions(int(x), int(y))
        elif cmd.startswith('move'):
            move, position, x, to, position2, y = cmdsplit
            self.move_positions(int(y), int(x))
        else:
            raise Exception(f'Invalid command {cmd}')
            
def scramble_password(password: str, instructions:List[str]) -> str:
    scambler = Scrambler(password)
    for instruction in instructions:
        scambler.parse_commands(instruction)
    return ''.join(scambler.password)


@session.submit_result(level=1, tests=[({'password': 'abcde', 'inp':[
    'swap position 4 with position 0',
    'swap letter d with letter b',
    'reverse positions 0 through 4',
    'rotate left 1 step',
    'move position 1 to position 4',
    'move position 3 to position 0',
    'rotate based on position of letter b',
    'rotate based on position of letter d',
]}, 'decab')])
def solve_part1(inp: List[str], password: str='abcdefgh'):
    return scramble_password(password, inp)

@session.submit_result(level=2)
def solve_part2(inp, password='fbgdceah'):
    good_passwords = set()
    for apass in permutations(password, len(password)):
        scrambled_password = scramble_password(apass, inp)
        if scrambled_password == password:
            good_passwords.add(''.join(apass))
    if len(good_passwords) == 1:
        good_pass, = good_passwords
        return good_pass
    else:
        print(good_passwords)


if __name__ == '__main__':
    inp = [i for i in session.read_input().split('\n') if i]
    
    solve_part1(inp)
    
    solve_part2(inp)
