

test_output_input_part1 = {
    6: ['R8,U5,L5,D3', 'U7,R6,D4,L4'],
    159: ['R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83'],
    135: ['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'],
}

def generate_coors(vect, ox, oy):
    dir, mag = vect[0], int(vect[1:])
    if dir == 'R':
        return [(x, oy) for x in range(ox+1, ox+1+mag)]
    elif dir == 'L':
        return [(x, oy) for x in range(ox-1, ox-1-mag, -1)]
    elif dir == 'U':
        return [(ox, y) for y in range(oy+1, oy+1+mag)]
    elif dir == 'D':
        return [(ox, y) for y in range(oy-1, oy-1-mag, -1)]

def add_wire_coors(wire_vect, wire_coors):
    for vect in wire_vect.split(','):
        wirex, wirey = wire_coors[-1]
        wire_coors.extend(generate_coors(vect, wirex, wirey))
    return wire_coors

def solve_part1(ds):
    wire1, wire2 = ds
    wire1_coors = add_wire_coors(wire1, [(0,0)])
    wire2_coors = add_wire_coors(wire2, [(0,0)])
    
    wire1_mht = [abs(x)+abs(y) for x, y in wire1_coors]
    wire2_mht = [abs(x)+abs(y) for x, y in wire2_coors]

    for mht1 in (set(wire1_mht) - {0}):
        for mht2 in (set(wire2_mht) - {0}):
            if mht2 > mht1:
                break
            elif mht2 < mht1:
                continue
            
            mht1_coors = [wire1_coors[i] for i in range(len(wire1_mht)) if wire1_mht[i] == mht1]
            mht2_coors = [wire2_coors[i] for i in range(len(wire2_mht)) if wire2_mht[i] == mht1]

            common_coors = [coor for coor in mht1_coors if coor in mht2_coors]
            if common_coors:
                return mht1
    return None


for output, input in test_output_input_part1.items():
    cal_output = solve_part1(input)
    assert output == cal_output, f'Expecting {output}, got {cal_output} instead.'




def solve_part2(ds):
    wire1, wire2 = ds
    wire1_coors = add_wire_coors(wire1, [(0,0)])
    wire2_coors = add_wire_coors(wire2, [(0,0)])
    
    wire1_mht = [abs(x)+abs(y) for x, y in wire1_coors]
    wire2_mht = [abs(x)+abs(y) for x, y in wire2_coors]

    common_mht = (set(wire1_mht) & set(wire2_mht)) - {0}

    total_steps = []
    for mht in common_mht:
        mht1_coors = [(wire1_coors[step], step) for step in range(len(wire1_mht)) if wire1_mht[step] == mht]
        mht2_coors = [(wire2_coors[step], step) for step in range(len(wire2_mht)) if wire2_mht[step] == mht]

        for mht1_coor, step1 in mht1_coors:
            for mht2_coor, step2 in mht2_coors:
                if mht1_coor == mht2_coor:
                    total_steps.append(step1+step2)
         
    return min(total_steps)

test_output_input_part2 = zip([30, 610, 410], test_output_input_part1.values())
for output, input in test_output_input_part2:
    cal_output = solve_part2(input)
    assert output == cal_output, f'Expecting {output}, got {cal_output} instead.'

print('Tests for part1 and part2 passed, the actual output of part1 of this problem is')
with open('2019/day3.txt', 'r') as f:
    lines = f.readlines()
    print(f'Part1: {solve_part1(lines)}')
    print(f'Part2: {solve_part2(lines)}')