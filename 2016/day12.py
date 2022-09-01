
from typing import Dict
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class Command:
    register: Dict = {c: 0 for c in 'abcd'}
    def __init__(self, cmd: str, x: str, y: str=None) -> None:
        self.cmd = cmd
        self.x = x
        self.y = y
    
    @classmethod
    def parse_command(cls, command: str) -> object:
        cmd_split = command.split(' ')
        if len(cmd_split) == 3:
            cmd, x, y = cmd_split
        elif len(cmd_split) == 2:
            cmd, x = cmd_split
            y = None
        else:
            raise Exception(f'Invalid command {command}')
        return cls(cmd, x, y)
    
    def evaluate(self):
        if self.cmd == 'cpy':
            if self.x.isnumeric():
                self.register[self.y] = int(self.x)
            else:
                self.register[self.y] = self.register[self.x]
        elif self.cmd == 'inc':
            self.register[self.x]+=1
        elif self.cmd == 'dec':
            self.register[self.x]-=1
        elif self.cmd == 'jnz':
            if self.x.isnumeric():
                if int(self.x) != 0:
                    return int(self.y)
            elif self.register[self.x] != 0:
                return int(self.y)
        else:
            raise Exception(f'Invalid cmd {self.cmd}')
        return 1

@session.submit_result(level=1, tests=[({'commands': [
    Command('cpy', '41', 'a'),
    Command('inc', 'a'),
    Command('inc', 'a'),
    Command('dec', 'a'),
    Command('jnz', 'a', '2'),
    Command('dec', 'a'),
]}, 42)])
def solve_part1(commands):
    c = 0
    while c < len(commands) and c >= 0:
        c += commands[c].evaluate()
    return Command.register['a']

@session.submit_result(level=2)
def solve_part2(commands):
    Command.register = {'a': 0, 'b': 0, 'c': 1, 'd': 0}
    c = 0
    while c < len(commands):
        c += commands[c].evaluate()
    return Command.register['a']


if __name__ == '__main__':
    commands = [Command.parse_command(i) for i in session.read_input().split('\n') if i]
    
    solve_part1(commands)
    
    solve_part2(commands)
