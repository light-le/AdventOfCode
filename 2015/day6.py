from utils import AdventSession, extract_year_day_from_path


def solve_part1(lights, coors):
    for start, end_coors in coors:
        if start.startswith('turn on'):
            start_coors = start.replace('turn on ', '')
            start_x, start_y = [int(s) for s in start_coors.split(',')]
            end_x, end_y = [int(s) for s in end_coors.split(',')]

            for x in range(start_x, end_x+1):
                for y in range(start_y, end_y+1):
                    lights[x][y] = 1
        elif start.startswith('turn off'):
            start_coors = start.replace('turn off ', '')
            start_x, start_y = [int(s) for s in start_coors.split(',')]
            end_x, end_y = [int(s) for s in end_coors.split(',')]

            for x in range(start_x, end_x+1):
                for y in range(start_y, end_y+1):
                    lights[x][y] = 0
        elif start.startswith('toggle'):
            start_coors = start.replace('toggle ', '')
            start_x, start_y = [int(s) for s in start_coors.split(',')]
            end_x, end_y = [int(s) for s in end_coors.split(',')]

            for x in range(start_x, end_x+1):
                for y in range(start_y, end_y+1):
                    lights[x][y] = abs(lights[x][y]-1)
        else:
            raise Exception(start)
    return sum([sum(row) for row in lights])


def solve_part2(lights, coors):
    for start, end_coors in coors:
        if start.startswith('turn on'):
            start_coors = start.replace('turn on ', '')
            start_x, start_y = [int(s) for s in start_coors.split(',')]
            end_x, end_y = [int(s) for s in end_coors.split(',')]

            for x in range(start_x, end_x+1):
                for y in range(start_y, end_y+1):
                    lights[x][y] += 1
        elif start.startswith('turn off'):
            start_coors = start.replace('turn off ', '')
            start_x, start_y = [int(s) for s in start_coors.split(',')]
            end_x, end_y = [int(s) for s in end_coors.split(',')]

            for x in range(start_x, end_x+1):
                for y in range(start_y, end_y+1):
                    lights[x][y] = max(lights[x][y]-1, 0)
        elif start.startswith('toggle'):
            start_coors = start.replace('toggle ', '')
            start_x, start_y = [int(s) for s in start_coors.split(',')]
            end_x, end_y = [int(s) for s in end_coors.split(',')]

            for x in range(start_x, end_x+1):
                for y in range(start_y, end_y+1):
                    lights[x][y] += 2
        else:
            raise Exception(start)
    return sum([sum(row) for row in lights])

if __name__ == '__main__':
    session = AdventSession(**extract_year_day_from_path(__file__))
    input = session.read_input()

    lines = input.split('\n')
    coors = [line.split(' through ') for line in lines if line != '']

    lights = [[0 for _ in range(1000)] for _ in range(1000)]

    part1_ans = solve_part1(lights, coors)
    print('Part1:', part1_ans)
    session.post_answer(part1_ans, level=1)

    lights = [[0 for _ in range(1000)] for _ in range(1000)]
    part2_ans = solve_part2(lights, coors)
    print('Part2: ', part2_ans)
    session.post_answer(part2_ans, level=2)

        
        