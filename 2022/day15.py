from typing import Tuple, Set, List
from functools import reduce
from functools import cached_property
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class Device:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        
    def manhattan_distant(self, x, y) -> int:
        return abs(self.x - x) + abs(self.y - y) 
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__} x={self.x} y={self.y}'
        
class Beacon(Device):
    pass

class Sensor(Device):
    def __init__(self, x: int, y: int, closest_beacon: Beacon) -> None:
        super().__init__(x, y)
        self.closest_beacon = closest_beacon
    
    @cached_property
    def mht_distant_of_closest_beacon(self) -> int:
        return self.manhattan_distant(self.closest_beacon.x, self.closest_beacon.y)
    
    def is_within_mht_of_closest_beacon(self, x, y) -> bool:
        return self.manhattan_distant(x, y) <= self.mht_distant_of_closest_beacon
    
    def x_spots_within_mht_of_closest_beacon(self, y: int) -> Set[int]:
        if abs(self.y - y) > self.mht_distant_of_closest_beacon:
            return set()
        abs_x_diffs =  self.mht_distant_of_closest_beacon - abs(self.y - y)
        
        x_spots = set()
        for abs_xdiff in range(abs_x_diffs+1):
            x_spots.add(self.x - abs_xdiff)
            x_spots.add(self.x + abs_xdiff)
        return x_spots
    
    def possible_distress_beacon_spots(self, limit: int) -> Set[Tuple[int, int]]:
        x_left = self.x - self.mht_distant_of_closest_beacon - 1
        y_top = self.y - self.mht_distant_of_closest_beacon - 1
        
        spots = set()
        
        # top left
        for x, y in zip(range(x_left, self.x+1), range(self.y, y_top-1, -1)):
            if 0<=x<=limit and 0<=y<=limit:
                spots.add((x, y))

        #top right
        x_right = self.x + self.mht_distant_of_closest_beacon + 1
        for x, y in zip(range(self.x, x_right+1), range(y_top, self.y+1)):
            if 0<=x<=limit and 0<=y<=limit:
                spots.add((x, y))
                
        # bottom right
        y_bottom = self.y + self.mht_distant_of_closest_beacon + 1
        for x, y in zip(range(x_right, self.x-1, -1), range(self.y, y_bottom+1)):
            if 0<=x<=limit and 0<=y<=limit:
                spots.add((x, y))
        
        # bottom left                
        for x, y in zip(range(self.x, x_left-1, -1), range(y_bottom, self.y-1, -1)):
            if 0<=x<=limit and 0<=y<=limit:
                spots.add((x, y))
        
        return spots
        
        
def parse_xy(xt: str, yt: str) -> Tuple[int, int]:
    xc, xv = xt[:-1].split('=')
    yc, yv = yt.split('=')
    return int(xv), int(yv)

def parse_line(txt: str) -> Sensor:
    sensor_text, beacon_text = txt.split(': ')
    sens, at, xt, yt = sensor_text.split(' ')
    senx, seny = parse_xy(xt, yt)
    
    clo, beac, is_, at_, xt, yt = beacon_text.split(' ')
    beax, beay = parse_xy(xt, yt)
    return Sensor(senx, seny, closest_beacon=Beacon(beax, beay))
    

@session.submit_result(level=1, tests=[({'inp': [
    'Sensor at x=2, y=18: closest beacon is at x=-2, y=15',
    'Sensor at x=9, y=16: closest beacon is at x=10, y=16',
    'Sensor at x=13, y=2: closest beacon is at x=15, y=3',
    'Sensor at x=12, y=14: closest beacon is at x=10, y=16',
    'Sensor at x=10, y=20: closest beacon is at x=10, y=16',
    'Sensor at x=14, y=17: closest beacon is at x=10, y=16',
    'Sensor at x=8, y=7: closest beacon is at x=2, y=10',
    'Sensor at x=2, y=0: closest beacon is at x=2, y=10',
    'Sensor at x=0, y=11: closest beacon is at x=2, y=10',
    'Sensor at x=20, y=14: closest beacon is at x=25, y=17',
    'Sensor at x=17, y=20: closest beacon is at x=21, y=22',
    'Sensor at x=16, y=7: closest beacon is at x=15, y=3',
    'Sensor at x=14, y=3: closest beacon is at x=15, y=3',
    'Sensor at x=20, y=1: closest beacon is at x=15, y=3'
], 'y': 10}, 26)])
def solve_part1(inp, y):
    sensors = [parse_line(line) for line in inp]
    closest_beacons = {sensor.closest_beacon for sensor in sensors}
    
    
    beacon_setx = {b.x for b in closest_beacons if b.y == y}
    
    x_spots = reduce((lambda sa, sb: sa|sb), [sensor.x_spots_within_mht_of_closest_beacon(y)
                                              for sensor in sensors])
    return len(x_spots - (x_spots & beacon_setx))

@session.submit_result(level=2, tests=[({'inp': [
    'Sensor at x=2, y=18: closest beacon is at x=-2, y=15',
    'Sensor at x=9, y=16: closest beacon is at x=10, y=16',
    'Sensor at x=13, y=2: closest beacon is at x=15, y=3',
    'Sensor at x=12, y=14: closest beacon is at x=10, y=16',
    'Sensor at x=10, y=20: closest beacon is at x=10, y=16',
    'Sensor at x=14, y=17: closest beacon is at x=10, y=16',
    'Sensor at x=8, y=7: closest beacon is at x=2, y=10',
    'Sensor at x=2, y=0: closest beacon is at x=2, y=10',
    'Sensor at x=0, y=11: closest beacon is at x=2, y=10',
    'Sensor at x=20, y=14: closest beacon is at x=25, y=17',
    'Sensor at x=17, y=20: closest beacon is at x=21, y=22',
    'Sensor at x=16, y=7: closest beacon is at x=15, y=3',
    'Sensor at x=14, y=3: closest beacon is at x=15, y=3',
    'Sensor at x=20, y=1: closest beacon is at x=15, y=3'
], 'limit': 20}, 56000011)])
def solve_part2(inp, limit):
    sensors = [parse_line(line) for line in inp]
    
    for sensor in sensors:
        possible_spots = sensor.possible_distress_beacon_spots(limit)
        for possible_spotx, possible_spoty in possible_spots:
            if not any([sensor.is_within_mht_of_closest_beacon(possible_spotx, possible_spoty)
                        for sensor in sensors]):
                return possible_spotx*4000000+possible_spoty
            
    
if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp, y=2000000)
    
    solve_part2(inp, limit=4000000)
