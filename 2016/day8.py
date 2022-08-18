from dataclasses import dataclass
from enum import Enum
from itertools import product
from typing import Any
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class Status(Enum):
    OFF = 0
    ON = 1
    
    def __str__(self) -> str:
        return '.' if self.value else ' '
    

@dataclass
class Pixel:
    row: int
    col: int
    screen: Any
    status: int = Status.OFF


class Screen:
    def __init__(self, w: int=50, t: int=6) -> None:
        self.width = w
        self.tall = t
        self.pixels = {
            (r, c): Pixel(r, c, self) for r, c in product(range(t), range(w))
        }
        
    def count_lit_pixels(self):
        return [pixel.status for pixel in self.pixels.values()].count(Status.ON)
    
    def turn_pixels_on(self, w: int, t: int):
        for c in range(w):
            for r in range(t):
                self.pixels[(r, c)].status = Status.ON
        
    def rotate_row(self, row: int, by: int):
        sby = by % self.width
        new_pixels = dict()
        for (r, c) in self.pixels:
            if r == row:
                if c >= sby:
                    new_pixels[(r, c)] = self.pixels[(r, c-sby)]
                else:
                    new_pixels[(r, c)] = self.pixels[(r, c-sby+self.width)]
        self.pixels.update(new_pixels)
        
    def rotate_column(self, col: int, by: int):
        sby = by % self.tall
        new_pixels = dict()
        for (r, c) in self.pixels:
            if c == col:
                if r >= sby:
                    new_pixels[(r, c)] = self.pixels[(r-sby, c)]
                else:
                    new_pixels[(r, c)] = self.pixels[(r-sby+self.tall, c)]
        self.pixels.update(new_pixels)
    
    def __repr__(self) -> str:
        display = '\n'
        for r in range(self.tall):
            display += ''.join([str(self.pixels[(r, c)].status) for c in range(self.width)]) + '\n'
        return display

    def parse_command(self, cmd: str):
        if cmd.startswith('rect'):
            rect, dims = cmd.split()
            w, t = dims.split('x')
            self.turn_pixels_on(int(w), int(t))
        elif cmd.startswith('rotate'):
            rotate, rowcol, xy, by, n = cmd.split()
            if rowcol == 'row':
                y, row = xy.split('=')
                self.rotate_row(int(row), by=int(n))
            elif rowcol == 'column':
                x, col = xy.split('=')
                self.rotate_column(int(col), by=int(n))
            else:
                raise Exception(f'Invalid row col {rowcol}')
        else:
            raise Exception(f'Invalid command {cmd}')
            
    


@session.submit_result(level=1, tests=[({
    'inp': [
        'rect 3x2',
        'rotate column x=1 by 1',
        'rotate row y=0 by 4',
        'rotate column x=1 by 1',
        'rect 2x2',
    ],
    'screen': Screen(w=7,t=3)
    }, 8)])
def solve_part1(inp, screen=Screen()):
    [screen.parse_command(i) for i in inp]
    return screen.count_lit_pixels()
    

@session.submit_result(level=2, print_only=True)
def solve_part2(inp):
    screen = Screen()
    [screen.parse_command(i) for i in inp]
    return screen


if __name__ == '__main__':
    inp = [i for i in session.read_input().split('\n') if i]
    
    solve_part1(inp)
    
    solve_part2(inp)
