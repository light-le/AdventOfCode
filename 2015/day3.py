from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

class Santa:
    def __init__(self) -> None:
        self.p = Point(0, 0)
    
    def left(self):
        self.p = Point(self.p.x-1, self.p.y)
    
    def right(self):
        self.p = Point(self.p.x+1, self.p.y)

    def up(self):
        self.p = Point(self.p.x, self.p.y+1)
        
    def down(self):
        self.p = Point(self.p.x, self.p.y-1)
        



if __name__ == '__main__':
    with open('2015/day3.txt') as f:
        line = f.readline()

    # ----Part1----
    santa = Santa()
    houses_visited = {santa.p}
    for char in line:
        if char == '>':
            santa.right()
        elif char == '<':
            santa.left()
        elif char == '^':
            santa.up()
        elif char == 'v':
            santa.down()
        else:
            raise Exception(f'Invalid direction character {char}')
        houses_visited.add(santa.p)

    print('Part1:', len(houses_visited))

    # ----Part2----

    santa = Santa()
    robo_santa = Santa()

    houses_visited2 = {santa.p}

    for c, char in enumerate(line):
        if c % 2 == 0:
            mover = santa
        else:
            mover = robo_santa
        
        if char == '>':
            mover.right()
        elif char == '<':
            mover.left()
        elif char == '^':
            mover.up()
        elif char == 'v':
            mover.down()
        else:
            raise Exception(f'Invalid direction character {char}')

        houses_visited2.add(mover.p)

    print('Part2:', len(houses_visited2))

    