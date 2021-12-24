from itertools import product
def parse_range(s):
    '''
    parse a string text like -50..50 to range(-50,51),
    taking into account of limitation (50, 50)
    '''
    front, end = [int(n) for n in s.split('..')]
    if max(front, end) < -50 or min(front, end) > 50:
        return range(0, 0)
    return range(max(min(front, end), -50),
                 min(max(front, end), 50) + 1)

def dict_cubes(cube_range, status):
    return {cube: status for cube in list(product(*cube_range.values()))}

def part1_solution(lines):
    initilization = []
    for on_off, coords in lines:
        coords = [c.split('=') for c in coords.split(',')]
        coords = {xyz: parse_range(r) for xyz, r in coords}
        initilization.append(
            {'switch': on_off, 'cubes': coords}
        )

    cubes = dict()
    for init in initilization:
        cubes.update(dict_cubes(init['cubes'], status=init['switch']))
    return len([cube for cube, status in cubes.items() if status == 'on'])

def parse_range_nolimit(s):
    front, end = [int(n) for n in s.split('..')]
    return range(min(front, end), max(front, end)+1)

class Cube:
    def __init__(self, rangex, rangey, rangez) -> None:
        self.rangex = rangex
        self.rangey = rangey
        self.rangez = rangez

    def volume(self):
        return len(self.rangex)*len(self.rangey)*len(self.rangez)

    def intersect(self, o):
        if max(self.rangex) < min(o.rangex) or min(self.rangex) > max(o.rangex):
            return False
        if max(self.rangey) < min(o.rangey) or min(self.rangey) > max(o.rangey):
            return False
        if max(self.rangez) < min(o.rangez) or min(self.rangez) > max(o.rangez):
            return False
        return True

    def intersect_volume(self, o):
        return len(set(self.rangex)&set(o.rangex))*len(set(self.rangey)&set(o.rangey))*len(set(self.rangz)&set(o.rangez))
        

def part2_solution(lines):
    '''
    scan all the smallest possible cubes defined by the instruction,
    Go for the latest instructions for these cubes, if it's on, then they are on
    '''
    reboot = []
    sub_coords = {
        'x': [],
        'y': [],
        'z': [],
    }
    for on_off, coords in lines:
        coords = [c.split('=') for c in coords.split(',')]
        coords = {xyz: parse_range_nolimit(r) for xyz, r in coords}
        reboot.append(
            {'switch': on_off, 'cubes': coords}
        )
        for k in sub_coords:
            sub_coords[k].extend([min(coords[k]), max(coords[k])+1])

    reboot.reverse()
    sorted_coords = {k: sorted(v) for k, v in sub_coords.items()}

    cubes = 0
    for x1, x2 in zip(sorted_coords['x'], sorted_coords['x'][1:]):
        print(x1)
        ins_x = [rb for rb in reboot if x1 in rb['cubes']['x']]
        for y1, y2 in zip(sorted_coords['y'], sorted_coords['y'][1:]):
            ins_y = [ins for ins in ins_x if y1 in ins['cubes']['y']]
            for z1, z2 in zip(sorted_coords['z'], sorted_coords['z'][1:]):
                ins_z = [ins for ins in ins_y if z1 in ins['cubes']['z']]
                if ins_z and ins_z[0]['switch'] == 'on':
                    cubes += (x2-x1)*(y2-y1)*(z2-z1)
    return cubes

if __name__ == "__main__":
    with open('2021/day22.txt', 'r') as f:
        lines = f.readlines()
        lines = [line.split(' ') for line in lines]
    print(part1_solution(lines))
    print(part2_solution(lines))