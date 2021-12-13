def parse_network(network):
    '''
    Convert from list of [A-B, B-C] to dict of connecting {A: [B], B: [A,C]}
    '''
    cons = {}
    for net in  network:
        cave_a, cave_b = net.split('-')
        if cave_a in cons:
            cons[cave_a].append(cave_b)
        else:
            cons[cave_a] = [cave_b]
        if cave_b in cons:
            cons[cave_b].append(cave_a)
        else:
            cons[cave_b] = [cave_a]
    return cons

def add_cave_to_path(path, cave, paths, cons):
    if cave == 'end':
        paths.append(path+[cave])
        return paths

    new_path = path + [cave]
    for next_cave in cons[cave]:
        if next_cave.isupper() or next_cave not in path:
            paths = add_cave_to_path(new_path, next_cave, paths, cons)
    return paths

def part1_solution(cons):
    paths = []
    for cave in cons['start']:
        paths = add_cave_to_path(['start'], cave, paths, cons)
    return len(paths)

def add_cave_to_path2(path, cave, paths, cons, small_cave_pass):
    if cave == 'end':
        paths.append(path+[cave])
        return paths

    new_path = path + [cave]
    for next_cave in cons[cave]:
        if next_cave.isupper() or next_cave not in path:
            paths = add_cave_to_path2(new_path, next_cave, paths, cons, small_cave_pass)
        elif next_cave != 'start' and not small_cave_pass:
            paths = add_cave_to_path2(new_path, next_cave, paths, cons, small_cave_pass=True)
    return paths

def part2_solution(cons):
    paths = []
    for cave in cons['start']:
        paths = add_cave_to_path2(['start'], cave, paths, cons, small_cave_pass=False)
    return len(paths)

if __name__ == "__main__":
    with open('2021/day12.txt', 'r') as f:
        network = f.read().rsplit()

    connectors = parse_network(network)
    print(part1_solution(connectors))
    print(part2_solution(connectors))