from copy import deepcopy

def fold_coors(coors, instruct):
    dir, mag = instruct
    if dir == 'x':
        for i, (x, y) in enumerate(coors):
            if x > mag:
                coors[i][0] = mag - (x - mag)
    else:
        for i, (x, y) in enumerate(coors):
            if y > mag:
                coors[i][1] = mag - (y - mag)
    return coors

def part1_solution(coors, ins):
    first_ins, *other_ins = ins

    new_coors = fold_coors(coors, first_ins)
    return len(set([(x,y) for x,y in new_coors]))

def draw_image(img = [['.', '#', '.'], ['#', '#', '#'], ['.', '#', '.']]):
    for row in img:
        print(''.join(row), end='\n')


def part2_solution(coors, ins):
    for instruct in ins:
        new_coors = fold_coors(coors, instruct)
        unique_coors = set([(x, y) for x, y in new_coors])
        coors = [[x, y] for x, y in unique_coors]

    xmax = max([c[0] for c in coors])+1
    ymax = max([c[1] for c in coors])+1
    image = [['.' for _ in range(xmax)] for _ in range(ymax)]
    for x, y in coors:
        image[y][x] = '#'
    draw_image(image)


if __name__ == '__main__':
    with open('2021/day13.txt', 'r') as f:
        lines = f.readlines()

    dots = lines[:lines.index('\n')]

    dot_clean = [dot.rstrip().split(',') for dot in dots]
    dot_coors = [[int(x), int(y)] for x, y in dot_clean]

    instructions = lines[lines.index('\n')+1:]
    clean_ins = [ins.split(' ')[-1].split('=') for ins in instructions]
    xy_ins = [(xy, int(v)) for xy, v in clean_ins]
    print(part1_solution(deepcopy(dot_coors), xy_ins))
    part2_solution(deepcopy(dot_coors), xy_ins)
