from typing import List
from enum import Enum
from dataclasses import dataclass
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

@dataclass
class You:
    row: int
    col: int
    facing: Direction
    
    def get_tile_in_front(self, boardmap: List[List[str]]):
        '''
        return row, col and value
        '''
        if self.facing in [Direction.UP, Direction.DOWN]:
            col = self.col
            row = self.row-1 if self.facing == Direction.UP else (self.row+1)%len(boardmap)
            if boardmap[row][col] == ' ':
                all_col_values = [ro[col] for ro in boardmap]
                
                row = (max([r for r, rv in enumerate(all_col_values) if rv in ['#', '.']])
                       if self.facing == Direction.UP else min([r for r, rv in enumerate(all_col_values) if rv in ['#', '.']]))
        elif self.facing in [Direction.LEFT, Direction.RIGHT]:
            row = self.row
            col = self.col-1 if self.facing == Direction.LEFT else (self.col+1)%len(boardmap[0])
            if boardmap[row][col] == ' ':
                col = (max([c for c, co in enumerate(boardmap[row]) if co in ['#', '.']])
                       if self.facing == Direction.LEFT else min([c for c, co in enumerate(boardmap[row]) if co in ['#', '.']]))
        return (row, col, boardmap[row][col])
    
    def solve(self, boardmap: List[List[str]], instruction: str, start_col: int):
        ins = 0
        while ins < len(instruction):
            if instruction[ins] in ['L', 'R']:
                dir_change = 1 if instruction[ins] == 'R' else -1
                self.facing = Direction((Direction[self.facing.name].value+dir_change)%len(Direction))
                ins+=1
            else:
                numstr = ''
                for j in range(ins, len(instruction)):
                    if instruction[j].isdigit():
                        numstr += instruction[j]
                    else:
                        j-=1
                        break
                ins = j+1
                steps_instruction = int(numstr)
                walked = 0
                for step in range(steps_instruction):
                    *coor, front_tile = self.get_tile_in_front(boardmap)
                    if front_tile == '#':
                        break
                    elif front_tile == '.':
                        if len(coor) == 2:
                            self.row, self.col = coor
                        elif len(coor) == 3:
                            self.row, self.col, self.facing = coor
                        else:
                            raise Exception(f'What is this? {coor}')
                        walked += 1
                    else:
                        raise Exception(f'Impossible tile {front_tile} at row {front_row} and col {front_col}. And you are {you}')
        return 1000*(self.row+1) + 4*(self.col+1) + self.facing.value
    
class You2(You):
    def get_tile_in_front(self, boardmap: List[List[str]]):
        facing = self.facing
        if self.facing == Direction.UP:
            col = self.col
            row = self.row-1
            if boardmap[row][col] == ' ':
                if col < 50: # from left side to back side
                    row = self.row - (50 - col)
                    col = 50
                    facing = Direction.RIGHT
                elif col < 100: # from topside to front side
                    row = 150+(col-50)
                    col = 0
                    facing = Direction.RIGHT
                elif col < 150: # from rightside to front side
                    col = self.col-100
                    row = 199
                    facing = Direction.UP
                else:
                    raise Exception(f'Impossible to move up with such row {row} and col {col}')
        elif self.facing == Direction.LEFT:
            row = self.row
            col = self.col-1
            if boardmap[row][col] == ' ':
                if row < 50: # from top to left
                    col = 0
                    row = 149 - row
                    facing = Direction.RIGHT
                elif row < 100: # from back to left
                    col = row-50
                    row = 100
                    facing = Direction.DOWN
                elif row < 150: # from left to top
                    col = 50
                    row = 49 - (row-100)
                    facing = Direction.RIGHT
                elif row < 200: # front to top
                    col = row - 100
                    row = 0
                    facing = Direction.DOWN
                else:
                    raise Exception(f'Impossible to move left with such row {row} and col {col}')
        elif self.facing == Direction.RIGHT:
            row = self.row
            col = (self.col+1)%len(boardmap[0])
            if boardmap[row][col] == ' ':
                if row < 50: # from right to bottom
                    col = 99
                    row = 149 - row
                    facing = Direction.LEFT
                elif row < 100: # from back to right
                    col = row + 50
                    row = 49
                    facing = Direction.UP
                elif row < 150: # from bottom to right
                    row = 149 - row
                    col = 149
                    facing = Direction.LEFT
                elif row < 200: # front to bottom
                    col = row - 100
                    row = 149
                    facing = Direction.UP
                else:
                    raise Exception(f'Impossible to move right with such row {row} and col {col}')
        elif self.facing == Direction.DOWN:
            col = self.col
            row = (self.row+1)%len(boardmap)
            if boardmap[row][col] == ' ':
                if col < 50: # front to right
                    col = col + 100
                    row = 0
                    facing = Direction.DOWN
                elif col < 100: # bottom to front
                    row = col + 100
                    col = 49
                    facing = Direction.RIGHT
                elif col < 150: # from right to back
                    row = col - 50
                    col = 99
                    facing = Direction.LEFT
                else:
                    raise Exception(f'Impossible to move down with such row {row} and col {col}')
        return (row, col, facing, boardmap[row][col])
    
def parse_boards(boards: List[str]):
    row_length = max(len(row) for row in boards)
    return [list(row + ' '*(row_length-len(row))) for row in boards]

@session.submit_result(level=1, tests=[({'boards': [
    '        ...#',
    '        .#..',
    '        #...',
    '        ....',
    '...#.......#',
    '........#...',
    '..#....#....',
    '..........#.',
    '        ...#....',
    '        .....#..',
    '        .#......',
    '        ......#.'],
    'instruction': '10R5L5R10L4R5L5'
}, 6032)])
def solve_part1(boards, instruction):
    boardmap = parse_boards(boards)
    start_col = boardmap[0].index('.')
    
    you = You(row=0, col=start_col, facing=Direction.RIGHT)
    return you.solve(boardmap, instruction, start_col)
            
@session.submit_result(level=2)
def solve_part2(boards, instruction):
    boardmap = parse_boards(boards)
    start_col = boardmap[0].index('.')
    
    you = You2(row=0, col=start_col, facing=Direction.RIGHT)
    return you.solve(boardmap, instruction, start_col)


if __name__ == '__main__':
    board, instruction = session.read_input().split('\n\n')
    boards = board.split('\n')
    instruction = instruction.replace('\n', '')
    
    solve_part1(boards.copy(), instruction)
    solve_part2(boards.copy(), instruction)
