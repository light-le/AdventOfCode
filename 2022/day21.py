from pprint import pprint
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

reversed_signs = {
    '+': '-',
    '-': '+',
    '*': '/',
    '/': '*'
}

class MathOps:
    opd = {}
    changed_keys = set()
    def __init__(self, a: str, op: str=None, b: str=None) -> None:
        self.a = a
        self.b = b
        self.op = op
        
    def __repr__(self) -> str:
        return f'{self.a} {self.op} {self.b}'
    
    def evaluate(self):
        if self.op:
            assert self.op in {'+', '-', '*', '/'}, f'What sign is this? {self.op}'
            return int(eval(f'{self.opd[self.a].evaluate()} {self.op} {self.opd[self.b].evaluate()}'))
        elif self.a.isdigit():
            return int(self.a)
        else:
            return self.opd[self.a].evaluate()
    
    @classmethod
    def parse_line(cls, line: str) -> object:
        key, val = line.split(': ')
        cls.opd[key] = cls(*val.split(' '))
        
    @classmethod
    def reverse_operations(cls, key: str = 'humn', stop_when=()) -> None:
        stopk1, stopk2 = stop_when
        if key == stopk1:
            cls.opd[key] = MathOps(stopk2)
            return
        elif key == stopk2:
            cls.opd[key] = MathOps(stopk1)
            return
        for k, op in cls.opd.items():
            if key == op.a:
                cls.opd.pop(k)
                cls.changed_keys.add(k)
                cls.opd[key] = MathOps(k, reversed_signs[op.op], op.b)
                break
            elif key == op.b:
                cls.opd.pop(k)
                cls.changed_keys.add(k)
                if op.op in {'+', '*'}:
                    cls.opd[key] = MathOps(k, reversed_signs[op.op], op.a)
                else:
                    cls.opd[key] = MathOps(op.a, op.op, k)
                break
        cls.reverse_operations(k, stop_when)
        
        
            
            

@session.submit_result(level=1, tests=[({'inp': [
    'root: pppw + sjmn',
    'dbpl: 5',
    'cczh: sllz + lgvd',
    'zczc: 2',
    'ptdq: humn - dvpt',
    'dvpt: 3',
    'lfqf: 4',
    'humn: 5',
    'ljgn: 2',
    'sjmn: drzm * dbpl',
    'sllz: 4',
    'pppw: cczh / lfqf',
    'lgvd: ljgn * ptdq',
    'drzm: hmdt - zczc',
    'hmdt: 32'
]}, 152)])
def solve_part1(inp):
    MathOps.opd = {}
    [MathOps.parse_line(line) for line in inp]
    return MathOps.opd['root'].evaluate()

@session.submit_result(level=2, tests=[({'inp': [
    'root: pppw + sjmn',
    'dbpl: 5',
    'cczh: sllz + lgvd',
    'zczc: 2',
    'ptdq: humn - dvpt',
    'dvpt: 3',
    'lfqf: 4',
    'humn: 5',
    'ljgn: 2',
    'sjmn: drzm * dbpl',
    'sllz: 4',
    'pppw: cczh / lfqf',
    'lgvd: ljgn * ptdq',
    'drzm: hmdt - zczc',
    'hmdt: 32'
]}, 301)])
def solve_part2(inp):
    MathOps.opd = {}
    [MathOps.parse_line(line) for line in inp]
    
    root_op = MathOps.opd.pop('root')
    MathOps.opd.pop('humn')
    MathOps.reverse_operations('humn', stop_when=(root_op.a, root_op.b))
    pprint(MathOps.opd)
    return MathOps.opd['humn'].evaluate()


if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)


'''
    'root: pppw + sjmn',
    'dbpl: 5',
    'lgvd: cczh - sllz',
    'zczc: 2',
    'humn: ptdq + dvpt',
    'dvpt: 3',
    'lfqf: 4',
    'ljgn: 2',
    'sjmn: drzm * dbpl',
    'sllz: 4',
    'cczh: pppw * lfqf',
    'ptdq: lgvd / ljgn',
    'drzm: hmdt - zczc',
    'hmdt: 32'
'''