from functools import reduce
from collections import Counter

class Range:
    def __init__(self, line) -> None:
        '''
        convert `x1,y1 -> x2,y2` to self
        '''
        fr, to = line.split(' -> ')
        self.x1, self.y1 = [int(coor) for coor in fr.split(',')]
        self.x2, self.y2 = [int(coor) for coor in to.split(',')]

    def __repr__(self) -> str:
        return f'range from {self.x1, self.y1} to {self.x2, self.y2}'


    def generate_coors(self):
        if self.x1 == self.x2:
            return [(self.x1, y) for y in range(min(self.y1, self.y2), max(self.y1, self.y2)+1)]
        elif self.y1 == self.y2:
            return [(x, self.y1) for x in range(min(self.x1, self.x2), max(self.x1, self.x2)+1)]
        elif abs(self.x1 - self.x2) == abs(self.y1 - self.y2):
            return [(x, y) for x, y in zip(specialized_range(self.x1, self.x2), specialized_range(self.y1, self.y2))]

def specialized_range(a,b):
    '''
    generate range from a to b, inclusively, even when a > b
    '''
    if a <= b:
        return list(range(a, b+1))
    else:
        return list(range(a, b-1, -1))

def count_overlapping_coordinates(lines):
    coordinates = [li.generate_coors() for li in lines]
    flatten_coors = reduce((lambda a,b: a+b), coordinates)
    coors_count = Counter(flatten_coors).most_common()
    overlap_coors = [coor for coor in coors_count if coor[1] > 1]
    return len(overlap_coors)

def part1_solution(ranges):
    verhor_lines = [ra for ra in ranges if (ra.x1 == ra.x2 or ra.y1 == ra.y2)]
    return count_overlapping_coordinates(verhor_lines)

def part2_solution(ranges):
    return count_overlapping_coordinates(ranges)

if __name__ == "__main__":
    with open('2021/day5.txt', 'r') as f:
        lines = f.read().rsplit(sep='\n')

    ranges = [Range(line) for line in lines]
    print(part1_solution(ranges))
    print(part2_solution(ranges))