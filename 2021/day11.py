from copy import deepcopy
from functools import reduce
def is_valid_surrouding(coor, map_len):
    '''
    detect if the 8 surrounding octopi are valid
    '''
    r, c = coor
    R, C = map_len
    if r < 0 or r >= R:
        return False
    if c < 0 or c >= C:
        return False
    return True

def part1_solution(octopi):
    flashes = 0
    for step in range(100):
        to_be_flashed = [] # list of (r, c)
        # first scan all the octs, add 1 to each of them
        for r, row in enumerate(octopi):
            for c, col in enumerate(row):
                if col == 9:
                    to_be_flashed.append((r, c))
                octopi[r][c]+=1

        # 2nd, take into accounts all the 10 (to be flashed), add 1 to surroundings
        while to_be_flashed:
            flashing = to_be_flashed.pop()
            flashes += 1
            rlash, clash = flashing
            for rl in range(rlash-1, rlash+2):
                for cl in range(clash-1, clash+2):
                    if is_valid_surrouding((rl, cl), (len(octopi), len(octopi[0]))) and not (rl == rlash and cl == clash):
                        octopi[rl][cl]+=1
                        if octopi[rl][cl] == 10:
                            to_be_flashed.append((rl, cl))

        # 3rd make all the flashed ones become 0:
        for r, row in enumerate(octopi):
            for c, col in enumerate(row):
                if col >= 10:
                    octopi[r][c] = 0
    return flashes
                
def part2_solution(octopi):
    oct_count = len(octopi) * len(octopi[0])
    for step in range(1000):
        step_flashes = 0
        to_be_flashed = [] # list of (r, c)
        # first scan all the octs, add 1 to each of them
        for r, row in enumerate(octopi):
            for c, col in enumerate(row):
                if col == 9:
                    to_be_flashed.append((r, c))
                octopi[r][c]+=1

        # 2nd, take into accounts all the 10 (to be flashed), add 1 to surroundings
        while to_be_flashed:
            flashing = to_be_flashed.pop()
            step_flashes += 1
            rlash, clash = flashing
            for rl in range(rlash-1, rlash+2):
                for cl in range(clash-1, clash+2):
                    if is_valid_surrouding((rl, cl), (len(octopi), len(octopi[0]))) and not (rl == rlash and cl == clash):
                        octopi[rl][cl]+=1
                        if octopi[rl][cl] == 10:
                            to_be_flashed.append((rl, cl))
        if step_flashes == oct_count:
            return step+1
        # 3rd make all the flashed ones become 0:
        for r, row in enumerate(octopi):
            for c, col in enumerate(row):
                if col >= 10:
                    octopi[r][c] = 0
    return 0



if __name__ == "__main__":
    with open('2021/day11.txt', 'r') as f:
        octopi = [[int(c) for c in row] for row in f.read().rsplit()]
    # print(part1_solution(deepcopy(octopi)))
    print(part2_solution(deepcopy(octopi)))