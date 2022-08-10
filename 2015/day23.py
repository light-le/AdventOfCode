from utils import AdventSession, extract_year_day_from_path

class Command:
    a = 0
    b = 0
    def __init__(self, cmd: str, target: str=None, n: int=None) -> None:
        self.cmd = cmd
        self.target = target
        self.n = n
        
    @classmethod
    def parse_command(cls, command: str):
        cmd_target, *after_comma = command.split(', ')
        if after_comma:
            [n] = after_comma
        else:
            n = 0
            
        cmd, target = cmd_target.split(' ')
        if cmd == 'jmp':
            return cls(cmd=cmd, target=None, n=int(target))
        else:
            return cls(cmd=cmd, target=target, n=int(n))
        
    def __repr__(self) -> str:
        return f'{self.cmd} {self.target} {str(self.n)}'
    
    def execute(self) -> int:
        cls = self.__class__
        if self.cmd == 'hlf':
            if self.target == 'a':
                cls.a //= 2
            elif self.target == 'b':
                cls.b //= 2
            else:
                raise Exception(f'incorrect target {self.target}')
            return 1
        elif self.cmd == 'tpl':
            if self.target == 'a':
                cls.a *= 3
            elif self.target == 'b':
                cls.b *= 3
            else:
                raise Exception(f'incorrect target {self.target}')
            return 1
        elif self.cmd == 'inc':
            if self.target == 'a':
                cls.a += 1
            elif self.target == 'b':
                cls.b += 1
            else:
                raise Exception(f'incorrect target {self.target}')
            return 1
        elif self.cmd == 'jmp':
            return self.n
        elif self.cmd == 'jie':
            if ((self.target == 'a' and self.a % 2 == 0) or
                (self.target == 'b' and self.b % 2 == 0)):
                return self.n
            return 1
        elif self.cmd == 'jio':
            if ((self.target == 'a' and self.a == 1) or
                (self.target == 'b' and self.b == 1)):
                return self.n
            return 1
        else:
            raise Exception(f'incorrect command {self.cmd}')
            
        
            
def solve_part(cmds):
    c = 0
    while c < len(cmds):
        c += cmds[c].execute()
    return Command.b
        
    
if __name__ == '__main__':
    session = AdventSession(**extract_year_day_from_path(__file__))
    
    commands = [Command.parse_command(cs) for cs in session.read_input().split('\n') if cs]
    
    part1_answer = solve_part(commands)
    print(part1_answer)
    session.post_answer(part1_answer, level=1)
    
    Command.a = 1
    Command.b = 0
    
    part2_answer = solve_part(commands)
    print(part2_answer)
    session.post_answer(part2_answer, level=2)
    