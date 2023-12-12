from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque

from utils import AdventSession, extract_year_day_from_path
    
    
session = AdventSession(**extract_year_day_from_path(__file__))

@dataclass
class Pipe:
    row: int#=field(repr=False)
    col: int#=field(repr=False)
    type: str
    connected_pipe1: Pipe=field(repr=False, default=None)
    connected_pipe2: Pipe=field(repr=False, default=None)
    min_steps_from_s: int=field(init=False, default=float('inf'))
    connected_to_s: bool=field(default=False)#, repr=False)
    
def find_s(lines: list[str]) -> tuple[int, int]:
    for l, line in enumerate(lines):
        if 'S' in line:
            return (l, line.index('S'))

def parse_pipeline(lines: list[str]) -> list[list[str]]:
    '''return a list of list of connected Pipe'''
    pipeline = list()
    for r, row in enumerate(lines):
        line = list()
        for c, char in enumerate(row):
            if char == '.' or char == 'S':
                line.append(char)
                continue
            
            prev_pipe = None
            pipe = Pipe(r, c, char)
            if char in ('|', 'L'):
                if r > 0 and isinstance(pipeline[-1][c], Pipe):
                    if pipeline[-1][c].type in ('|', '7', 'F'):
                        prev_pipe = pipeline[-1][c]
            elif char in ('-', '7'):
                if c > 0 and isinstance(line[-1], Pipe):
                    if line[-1].type in ('L', '-', 'F'):
                        prev_pipe = line[-1]
            elif char == 'J':
                if r > 0 and isinstance(pipeline[-1][c], Pipe):
                    if pipeline[-1][c].type in ('|', '7', 'F'):
                        prev_pipe = pipeline[-1][c]
                        pipe.connected_pipe1 = prev_pipe
                        if prev_pipe.connected_pipe1 is None:
                            prev_pipe.connected_pipe1 = pipe
                        else:
                            prev_pipe.connected_pipe2 = pipe

                if c > 0 and isinstance(line[-1], Pipe):
                    if line[-1].type in ('-', 'F', 'L'):
                        prev_pipe = line[-1]
                        if pipe.connected_pipe1 is None:
                            pipe.connected_pipe1 = prev_pipe
                        else:
                            pipe.connected_pipe2 = prev_pipe
                            
                        if prev_pipe.connected_pipe1 is None:
                            prev_pipe.connected_pipe1 = pipe
                        else:
                            prev_pipe.connected_pipe2 = pipe
                        
                        
                prev_pipe = None
                    

            if prev_pipe:
                pipe.connected_pipe1 = prev_pipe
                if prev_pipe.connected_pipe1 is None:
                    prev_pipe.connected_pipe1 = pipe
                else:
                    prev_pipe.connected_pipe2 = pipe
            
                
            line.append(pipe)
        pipeline.append(line)
    return pipeline
            
            

    

@session.submit_result(level=1, tests=[({'inp':[
    '.....',
    '.S-7.',
    '.|.|.',
    '.L-J.',
    '.....',
]}, 4), ({'inp': [
    '..F7.',
    '.FJ|.',
    'SJ.L7',
    '|F--J',
    'LJ...',
]}, 8)])
def solve_part1(inp: list[str]):
    srow, scol = find_s(inp)
    pipeline = parse_pipeline(inp)
    
    connected_to_s = []
    if srow > 0 and isinstance(pipeline[srow-1][scol], Pipe) and pipeline[srow-1][scol].type in ('|', '7', 'F'):
        connected_to_s.append(pipeline[srow-1][scol])
    if srow < len(inp)-1 and isinstance(pipeline[srow+1][scol], Pipe) and pipeline[srow+1][scol].type in ('|', 'L', 'J'):
        connected_to_s.append(pipeline[srow+1][scol])
    if scol > 0 and isinstance(pipeline[srow][scol-1], Pipe) and pipeline[srow][scol-1].type in ('-', 'F', 'L'):
        connected_to_s.append(pipeline[srow][scol-1])
    if scol < len(inp[0])-1 and isinstance(pipeline[srow][scol+1], Pipe) and pipeline[srow][scol+1].type in ('-', '7', 'J'):
        connected_to_s.append(pipeline[srow][scol+1])
    
    for pipe in connected_to_s:
        pipe.min_steps_from_s = 1
    
    pipe_queue = deque(connected_to_s)
    max_steps = 0
    
    while pipe_queue:
        pipe = pipe_queue.popleft()
        next_pipe_steps = pipe.min_steps_from_s + 1
        next_pipe = None
        if pipe.connected_pipe1 and next_pipe_steps < pipe.connected_pipe1.min_steps_from_s:
            next_pipe = pipe.connected_pipe1
        elif pipe.connected_pipe2 and next_pipe_steps < pipe.connected_pipe2.min_steps_from_s:
            next_pipe = pipe.connected_pipe2
        
        if next_pipe:
            next_pipe.min_steps_from_s = next_pipe_steps
            pipe_queue.append(next_pipe)
            max_steps = max(max_steps, next_pipe_steps)
    return max_steps
        
        
@session.submit_result(level=2, tests=[({'inp': [
    '..........',
    '.S------7.',
    '.|F----7|.',
    '.||....||.',
    '.||....||.',
    '.|L-7F-J|.',
    '.|..||..|.',
    '.L--JL--J.',
    '..........'
]}, 4), ({'inp': [
    '.F----7F7F7F7F-7....',
    '.|F--7||||||||FJ....',
    '.||.FJ||||||||L7....',
    'FJL7L7LJLJ||LJ.L-7..',
    'L--J.L7...LJS7F-7L7.',
    '....F-J..F7FJ|L7L7L7',
    '....L7.F7||L7|.L7L7|',
    '.....|FJLJ|FJ|F7|.LJ',
    '....FJL-7.||.||||...',
    '....L---J.LJ.LJLJ...'
]}, 8), ({'inp': [
    'FF7FSF7F7F7F7F7F---7',
    'L|LJ||||||||||||F--J',
    'FL-7LJLJ||||||LJL-77',
    'F--JF--7||LJLJ7F7FJ-',
    'L---JF-JLJ.||-FJLJJ7',
    '|F|F-JF---7F7-L7L|7|',
    '|FFJF7L7F-JF7|JL---7',
    '7-L-JL7||F7|L7F-7F7|',
    'L.L7LFJ|||||FJL7||LJ',
    'L7JLJL-JLJLJL--JLJ.L'
]}, 10)])
def solve_part2(inp: list[str]):
    srow, scol = find_s(inp)
    pipeline = parse_pipeline(inp)
    
    s_shapes = []
    connected_to_s = []
    
    if srow > 0 and isinstance(pipeline[srow-1][scol], Pipe) and pipeline[srow-1][scol].type in ('|', '7', 'F'):
        connected_to_s.append(pipeline[srow-1][scol])
        s_shapes.append('up')
    if srow < len(inp)-1 and isinstance(pipeline[srow+1][scol], Pipe) and pipeline[srow+1][scol].type in ('|', 'L', 'J'):
        connected_to_s.append(pipeline[srow+1][scol])
        s_shapes.append('down')
    if scol > 0 and isinstance(pipeline[srow][scol-1], Pipe) and pipeline[srow][scol-1].type in ('-', 'F', 'L'):
        connected_to_s.append(pipeline[srow][scol-1])
        s_shapes.append('left')
    if scol < len(inp[0])-1 and isinstance(pipeline[srow][scol+1], Pipe) and pipeline[srow][scol+1].type in ('-', '7', 'J'):
        connected_to_s.append(pipeline[srow][scol+1])
        s_shapes.append('right')
        
    sconnected_pipe1, sconnected_pipe2 = connected_to_s

    sorted_sshapes = tuple(sorted(s_shapes))
    sorted_shape_types = {
        ('left', 'up'): 'J',
        ('down', 'up'): '|',
        ('right', 'up'): 'L',
        ('down', 'left'): '7',
        ('down', 'right'): 'F',
        ('left', 'right'): '-'
    }
    
    
    s_pipe = Pipe(srow, scol, sorted_shape_types[sorted_sshapes],
                  connected_pipe1=sconnected_pipe1,
                  connected_pipe2=sconnected_pipe2,
                  connected_to_s=True)
    pipeline[srow][scol] = s_pipe
    
    sconnected_pipe1.connected_pipe1 = sconnected_pipe1.connected_pipe1 or s_pipe
    sconnected_pipe1.connected_pipe2 = sconnected_pipe1.connected_pipe2 or s_pipe
    sconnected_pipe1.connected_to_s = True
    
    sconnected_pipe2.connected_pipe1 = sconnected_pipe2.connected_pipe1 or s_pipe
    sconnected_pipe2.connected_pipe2 = sconnected_pipe2.connected_pipe2 or s_pipe
    sconnected_pipe2.connected_to_s = True
    
    
    pipe = sconnected_pipe1.connected_pipe1 if not sconnected_pipe1.connected_pipe1.connected_to_s else sconnected_pipe1.connected_pipe2
    pipe.connected_to_s = True
    
    while not pipe.connected_pipe1.connected_to_s or not pipe.connected_pipe2.connected_to_s:
        pipe = pipe.connected_pipe1 if not pipe.connected_pipe1.connected_to_s else pipe.connected_pipe2
        pipe.connected_to_s = True
    
    insider_count = 0
    for row in pipeline[1:-1]:
        for i, item in enumerate(row[1:-1]):
            if item == '.' or not item.connected_to_s:
                righties = row[i+1:]
                northern_pipes = [pipe for pipe in righties if isinstance(pipe, Pipe) and pipe.type in ('|', 'L', 'J') and pipe.connected_to_s]
                insider_count += (len(northern_pipes) % 2)
    return insider_count
                

if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
