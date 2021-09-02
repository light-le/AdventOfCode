
part1_inputs = [
    'B)C',
    'E)J',
    'B)G',
    'D)I',
    'C)D',
    'K)L',
    'E)F',
    'G)H',
    'J)K',
    'COM)B',
    'D)E',
]

class Orbital:
    def __init__(self, label, rank=0, parent=None) -> None:
        self.label = label
        self._rank = rank
        self._parent = parent
        self.children = []

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, new_rank):
        self._rank = new_rank
        for child in self.children:
            child.rank = new_rank + 1
    
    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent


    def add_child(self, child):
        child.rank = self.rank + 1
        self.children.append(child)

    def sum_ranks_below(self):
        base = self.rank
        for child in self.children:
            base += child.sum_ranks_below()
        return base

    def __repr__(self) -> str:
        return f'{self.label}{self.rank}'

    def path_to_root(self):
        if self.parent:
            return [self.parent.label] + self.parent.path_to_root()
        else:
            return []


def prepare(inps):
    orbital_mapping = dict()
    for inp in inps:
        parent, child = inp.split(')')
        if parent not in orbital_mapping:
            orbital_mapping[parent] = Orbital(parent)
        if child not in orbital_mapping:
            orbital_mapping[child] = Orbital(child)
        orbital_mapping[parent].add_child(orbital_mapping[child])
        orbital_mapping[child].parent = orbital_mapping[parent]
    return orbital_mapping


def solve_part1(inps):
    orbital_mapping = prepare(inps)
    return orbital_mapping['COM'].sum_ranks_below()


def solve_part2(inps):
    orbital_mapping = prepare(inps)
    you_to_root = orbital_mapping["YOU"].path_to_root()
    santa_to_root = orbital_mapping["SAN"].path_to_root()
    
    for you_step, you_orbit in enumerate(you_to_root):
        for san_step, san_orbit in enumerate(santa_to_root):
            if you_orbit == san_orbit:
                return you_step + san_step

print('part1 test: ', solve_part1(part1_inputs))
print('part2 test: ', solve_part2(part1_inputs + ['K)YOU', 'I)SAN']))

with open('day6.txt', 'r') as f:
    lines = [line.rstrip() for line in f.readlines()]
    print('part1 real: ', solve_part1(lines))
    print('part2 real: ', solve_part2(lines))
