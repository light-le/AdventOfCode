
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

def parse_move(m: str) -> tuple[str, int]:
    dir, steps = m.split()
    return dir, int(steps)

class HeadTail:
    '''
    a pair of head and tail always following each other
    '''
    def __init__(self) -> None:
        self._hx = 0
        self._hy = 0
        self._tx = 0
        self._ty = 0
    
    def is_touching(self):
        return abs(self.hx - self.tx) <= 1 and abs(self.hy - self.ty) <= 1
    
    def tail_follow_head(self):
        if self.hx == self.tx:
            self.ty += (self.hy - self.ty)//abs(self.hy - self.ty)
        elif self.hy == self.ty:
            self.tx += (self.hx - self.tx)//abs(self.hx - self.tx)
        else: # move diagonal
            self.ty += (self.hy - self.ty)//abs(self.hy - self.ty)
            self.tx += (self.hx - self.tx)//abs(self.hx - self.tx)
            
    
    @property
    def hx(self):
        return self._hx
    
    @hx.setter
    def hx(self, x: int):
        self._hx = x
        if not self.is_touching():
            self.tail_follow_head()
        
    @property
    def hy(self):
        return self._hy
    
    @hy.setter
    def hy(self, y:int):
        self._hy = y
        if not self.is_touching():
            self.tail_follow_head()
        
    @property
    def tx(self):
        return self._tx
    
    @tx.setter
    def tx(self, x: int):
        self._tx = x
        
    @property
    def ty(self):
        return self._ty
    
    @ty.setter
    def ty(self, y:int):
        self._ty = y

@session.submit_result(level=1, tests=[({'inp': [
    'R 4',
    'U 4',
    'L 3',
    'D 1',
    'R 4',
    'D 1',
    'L 5',
    'R 2',
]}, 13)])
def solve_part1(inp):
    ht = HeadTail()
    tail_spots = {(0, 0)}
    
    for hmove in inp:
        dir, steps = parse_move(hmove)
        for _ in range(steps):
            if dir == 'R':
                ht.hx += 1
            elif dir == 'L':
                ht.hx -= 1
            elif dir == 'U':
                ht.hy += 1
            elif dir == 'D':
                ht.hy -= 1
            else:
                raise Exception(f'Invalid direction {dir}')
            tail_spots.add((ht.tx, ht.ty))
    return len(tail_spots)
        
class Knot:
    def __init__(self, x: int=0, y: int=0, prev: object=None, next: object=None) -> None:
        self._x = x
        self._y = y
        self.prev = prev
        self.next = next
        
    def __repr__(self) -> str:
        return f'{self.x} {self.y} ({self.next})'
        
    def is_touching_next(self) -> bool:
        if self.next is None:
            return True
        return abs(self.x - self.next.x) <= 1 and abs(self.y - self.next.y) <= 1
    
    def add_next_knot(self, knot: object):
        self.next = knot
        knot.prev = self
        
    def follow_prev_knot(self):
        if self.prev.x == self.x:
            self.y += (self.prev.y - self.y)//abs(self.prev.y - self.y)
        elif self.prev.y == self.y:
            self.x += (self.prev.x - self.x)//abs(self.prev.x - self.x)
        else: # move diagonal
            self._y += (self.prev.y - self.y)//abs(self.prev.y - self.y)
            self.x +=  (self.prev.x - self.x)//abs(self.prev.x - self.x)
        
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, new_x: int):
        self._x = new_x
        if not self.is_touching_next():
            self.next.follow_prev_knot()
        
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, new_y: int):
        self._y = new_y
        if not self.is_touching_next():
            self.next.follow_prev_knot()
        
@session.submit_result(level=2, tests=[({'inp': [
    'R 5',
    'U 8',
    'L 8',
    'D 3',
    'R 17',
    'D 10',
    'L 25',
    'U 20',
]}, 36)])
def solve_part2(inp):
    head = Knot()
    current = head
    for k in range(9):
        new_knot = Knot()
        current.add_next_knot(new_knot)
        current = new_knot
    
    last_knot = current
    
    last_spots = {(0,0)}
        
    for move in inp:
        dir, steps = parse_move(move)
        for step in range(steps):
            if dir == 'R':
                head.x += 1
            elif dir == 'L':
                head.x -= 1
            elif dir == 'U':
                head.y += 1
            elif dir == 'D':
                head.y -= 1
            else:
                raise Exception(f'Invalid direction {dir}')
            last_spots.add((last_knot.x, last_knot.y))
    return len(last_spots)
                
        
    

if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
