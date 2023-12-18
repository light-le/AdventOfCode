from __future__ import annotations
from heapq import heappop, heappush
from dataclasses import dataclass, field
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))



@dataclass(order=True, eq=True, frozen=True)
class Crucible:
    loss_and_distance: int
    total_heatloss: int
    row: int
    col: int
    dir: str=field(default=None, repr=False)
    dir_count: int=field(default=None, repr=False)
    
    def get_possible_next_options(self,
                                  tr: int, tc: int,
                                  visited_spots: set[tuple[int, int]],
                                  map: list[list[int]]) -> set[Crucible]:
        options = self._get_surroundings(tr, tc)
        
        return self._possible_options(tr, tc, visited_spots, map, options)

    def _possible_options(self, tr, tc, visited_spots, map, options):
        possible_next_paths = set()
        for r, c, dir in options:
            if dir == self.dir:
                next_dir_count = self.dir_count + 1
            else:
                next_dir_count = 1
            
            next_heatloss = self.total_heatloss + map[r][c]
            next_loss_and_distance = next_heatloss + (tr-1-r) + (tc-1-c)
            # if next_loss_and_distance > 1265: # hardcoded for faster processing time
            #     continue
            next_path = Crucible(next_loss_and_distance, next_heatloss, r, c , dir, next_dir_count)
            if (r, c, dir, next_heatloss) not in visited_spots:
                possible_next_paths.add(next_path)
                visited_spots[(r, c, dir, next_heatloss)] = next_dir_count
            elif visited_spots[(r, c, dir, next_heatloss)] > next_dir_count:
                possible_next_paths.add(next_path)
                visited_spots[((r, c, dir, next_heatloss))] = next_dir_count
        return possible_next_paths

    def _get_surroundings(self, tr, tc):
        options = set()
        if self.row > 0 and not (self.dir_count == 3 and self.dir == '^') and self.dir != 'v':
            options.add((self.row-1, self.col, '^'))
        if self.col > 0 and not (self.dir_count == 3 and self.dir == '<') and self.dir != '>':
            options.add((self.row, self.col-1, '<'))
        if self.row < (tr-1) and not (self.dir_count == 3 and self.dir == 'v') and self.dir != '^':
            options.add((self.row+1, self.col, 'v'))
        if self.col < (tc-1) and not (self.dir_count == 3 and self.dir == '>') and self.dir != '<':
            options.add((self.row, self.col+1, '>'))
        return options
        
class UltraCrucible(Crucible):
    def get_possible_next_options(self,
                                  tr: int, tc: int,
                                  visited_spots: dict,
                                  map: list[list[int]]) -> set[Crucible]:
        
        options = set()
        
        if not (self.dir_count == 10 and self.dir == '^') and self.dir != 'v':
            if self.dir == '^' and self.row > 0:
                options.add((self.row-1, self.col, '^', 1, map[self.row-1][self.col]))
            elif self.dir != '^' and self.row > 3:
                options.add((self.row-4, self.col, '^', 4, sum(map[r][self.col] for r in range(self.row-4, self.row))))
                
                
        if not (self.dir_count == 10 and self.dir == '<') and self.dir != '>':
            if self.dir == '<' and self.col > 0:
                options.add((self.row, self.col-1, '<', 1, map[self.row][self.col-1]))
            elif self.dir != '<' and self.col > 3:
                options.add((self.row, self.col-4, '<', 4, sum(map[self.row][c] for c in range(self.col-4, self.col))))
                
                
        if not (self.dir_count == 10 and self.dir == 'v') and self.dir != '^':
            if self.dir == 'v' and self.row < tr-1:
                options.add((self.row+1, self.col, 'v', 1, map[self.row+1][self.col]))
            elif self.dir != 'v' and self.row < tr-4:
                options.add((self.row+4, self.col, 'v', 4, sum(map[r][self.col] for r in range(self.row+1, self.row+5))))
                
                
        if not (self.dir_count == 10 and self.dir == '>') and self.dir != '<':
            if self.dir == '>' and self.col < tc-1:
                options.add((self.row, self.col+1, '>', 1, map[self.row][self.col+1]))
            elif self.dir != '>' and self.col < tc-4:
                options.add((self.row, self.col+4, '>', 4, sum(map[self.row][c] for c in range(self.col+1, self.col+5))))
        
        possible_next_paths = set()
        for r, c, dir, steps, sum_heatloss in options:
            if dir == self.dir:
                next_dir_count = self.dir_count + steps
            else:
                next_dir_count = steps
            
            next_heatloss = self.total_heatloss + sum_heatloss
            next_loss_and_distance = next_heatloss + (tr-1-r) + (tc-1-c)
            
            if next_loss_and_distance > 1440:
                continue
            
            next_path = UltraCrucible(next_loss_and_distance, next_heatloss, r, c , dir, next_dir_count)
            if (r, c, dir, next_dir_count) not in visited_spots:
                possible_next_paths.add(next_path)
                visited_spots[(r, c, dir, next_dir_count)] = next_heatloss
            elif visited_spots[(r, c, dir, next_dir_count)] > next_heatloss:
                possible_next_paths.add(next_path)
                visited_spots[((r, c, dir, next_dir_count))] = next_heatloss
        return possible_next_paths
        

    
@session.submit_result(level=1, tests=[({'inp': [
    '2413432311323',
    '3215453535623',
    '3255245654254',
    '3446585845452',
    '4546657867536',
    '1438598798454',
    '4457876987766',
    '3637877979653',
    '4654967986887',
    '4564679986453',
    '1224686865563',
    '2546548887735',
    '4322674655533'
]}, 102)], wrong_answers={1267, 1266, 1189, 1265})
def solve_part1(inp: list[str]):
    heats = [[int(s) for s in line] for line in inp]
    
    total_rows = len(inp)
    total_cols = len(inp[0])
    
    visited_paths = dict()
    frontier = []
    heappush(frontier, Crucible(total_rows-1+total_cols-1, 0, 0, 0))
    
    finalist = float('inf')
    
    while frontier:
        path = heappop(frontier)
        visited_paths[(path.row, path.col, path.dir, path.total_heatloss)] = 0
        print(path)
        if path.total_heatloss >= finalist:
            print(frontier[:10])
            return finalist

        next_possible_options = path.get_possible_next_options(
            total_rows,
            total_cols,
            visited_paths,
            heats
        )
        
        for next_path in next_possible_options:
            if next_path.row == (total_rows-1) and next_path.col == (total_cols-1):
                finalist = min(finalist, next_path.total_heatloss)
            heappush(frontier, next_path)
    
@session.submit_result(level=2, tests=[({'inp': [
    '2413432311323',
    '3215453535623',
    '3255245654254',
    '3446585845452',
    '4546657867536',
    '1438598798454',
    '4457876987766',
    '3637877979653',
    '4654967986887',
    '4564679986453',
    '1224686865563',
    '2546548887735',
    '4322674655533'
]}, 94), ({'inp': [
    '111111111111',
    '999999999991',
    '999999999991',
    '999999999991',
    '999999999991'
]}, 71)], wrong_answers={
    1422,
    1440, # too high
    1480, # too high
    1470, # too high
})
def solve_part2(inp: list[str]):
    heats = [[int(s) for s in line] for line in inp]
    
    total_rows = len(inp)
    total_cols = len(inp[0])
    
    visited_paths = dict()
    frontier = []
    heappush(frontier, UltraCrucible(total_rows-1+total_cols-1, 0, 0, 0))
    
    finalist = float('inf')
    
    while frontier:
        path = heappop(frontier)
        visited_paths[(path.row, path.col, path.dir, 0)] = 0
        print(path)
        if path.total_heatloss >= finalist:
            print(frontier[:10])
            return finalist

        next_possible_options = path.get_possible_next_options(
            total_rows,
            total_cols,
            visited_paths,
            heats
        )
        
        for next_path in next_possible_options:
            if next_path.row == (total_rows-1) and next_path.col == (total_cols-1):
                finalist = min(finalist, next_path.total_heatloss)
            heappush(frontier, next_path)


if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
