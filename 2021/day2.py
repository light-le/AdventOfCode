
def part1_solution(cmds):
    hor = 0
    depth = 0
    for cmd in cmds:
        clean_cmd = cmd.rstrip()
        dir, mag = clean_cmd.split(' ')
        if dir == 'forward':
            hor += int(mag)
        elif dir == 'up':
            depth -= int(mag)
        elif dir == 'down':
            depth += int(mag)
        else:
            raise ValueError('Unexpected direction ', dir)
    return hor*depth

def part2_solution(cmds):
    hor = 0
    depth = 0
    aim = 0
    for cmd in cmds:
        clean_cmd = cmd.rstrip()
        dir, mag = clean_cmd.split(' ')
        if dir == 'forward':
            hor += int(mag)
            depth += aim*int(mag)
        elif dir == 'up':
            aim -= int(mag)
        elif dir == 'down':
            aim += int(mag)
        else:
            raise ValueError('Unexpected direction ', dir)
    return hor*depth

if __name__ == "__main__":
    with open('2021/day2.txt', 'r') as f:
        cmds = f.readlines()
    print(part1_solution(cmds))
    print(part2_solution(cmds))
