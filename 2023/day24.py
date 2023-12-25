from __future__ import annotations
from itertools import combinations
from math import sqrt
from dataclasses import dataclass
import numpy as np
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

@dataclass(frozen=True, eq=True)
class Vector:
    x: int
    y: int
    z: int
    
    def __add__(self, o: Vector) -> Vector:
        return Vector(self.x + o.x, self.y + o.y, self.z + o.z)
    
    def __sub__(self, o: Vector) -> Vector:
        return Vector(self.x - o.x, self.y - o.y, self.z - o.z)
    
    def __neg__(self) -> Vector:
        return Vector(-self.x, -self.y, -self.z)
    
    def __matmul__(self, o: Vector) -> Vector:
        '''Basically a cross product'''
        return Vector(self.y*o.z - self.z*o.y, self.z*o.x - self.x*o.z, self.x*o.y-self.y*o.x)
    
@dataclass
class Hailstone:
    position: Vector
    velocity: Vector
    
    def __post_init__(self) -> None:
        self.slope_m = self.velocity.y/self.velocity.x
        self.b = self.position.y - self.position.x*self.slope_m
        
    @classmethod
    def parse_line(self, line: str) -> Hailstone:
        postr, velostr = line.split(' @ ')
        
        position = Vector(*[int(s) for s in postr.split(', ')])
        velocity = Vector(*[int(s) for s in velostr.split(', ')])
        return Hailstone(position, velocity)
    
    def intersect(self, hail: Hailstone) -> tuple[int,int]:
        if self.slope_m == hail.slope_m: # parallel
            return None
        
        # m1*x + b1 = m2*x+b2 -> x(m1-m2) = b2 - b1 -> x = (b2 - b1) / (m1-m2)
        inter_x = (hail.b - self.b)/(self.slope_m - hail.slope_m)
        inter_y = self.slope_m*inter_x + self.b
        
        if any([
            (inter_x - self.position.x)/self.velocity.x < 0,
            (inter_x - hail.position.x)/hail.velocity.x < 0,
            (inter_y - self.position.y)/self.velocity.y < 0,
            (inter_y - hail.position.y)/hail.velocity.y < 0
        ]):
            return None
        
        return inter_x, inter_y
    
    


@session.submit_result(level=1, tests=[({'inp': [
    '19, 13, 30 @ -2,  1, -2',
    '18, 19, 22 @ -1, -1, -2',
    '20, 25, 34 @ -2, -2, -4',
    '12, 31, 28 @ -1, -2, -1',
    '20, 19, 15 @  1, -5, -3'
], 'range': (7, 27)}, 2)])
def solve_part1(inp: list[str], range: tuple[int, int]=(200000000000000, 400000000000000)) -> int:
    hails = [Hailstone.parse_line(line) for line in inp]
    
    startr, stopr = range
    
    count = 0
    for hail1, hail2 in combinations(hails, 2):
        intersect = hail1.intersect(hail2)
        if intersect:
            inter_x, inter_y = intersect
            if startr <= inter_x <= stopr and startr <= inter_y <= stopr:
                count += 1
    return count
    
@dataclass(frozen=True, eq=True)
class Hailstone2:
    position: Vector
    velocity: Vector
    
    @classmethod
    def parse_line(self, line: str) -> Hailstone2:
        postr, velostr = line.split(' @ ')
        
        position = Vector(*[int(s) for s in postr.split(', ')])
        velocity = Vector(*[int(s) for s in velostr.split(', ')])
        return Hailstone2(position, velocity)
    
    def mht_distance(self, hail: Hailstone2) -> int:
        return abs(self.position.x - hail.position.x) + abs(self.position.y - hail.position.y) + abs(self.position.z - hail.position.z)


@session.submit_result(level=2, tests=[({'inp': [
    '19, 13, 30 @ -2,  1, -2',
    '18, 19, 22 @ -1, -1, -2',
    '20, 25, 34 @ -2, -2, -4',
    '12, 31, 28 @ -1, -2, -1',
    '20, 19, 15 @  1, -5, -3'
]}, 47)])
def solve_part2_old(inp: list[str]) -> int:
    hails = [Hailstone2.parse_line(line) for line in inp]
    
    hail_distances = {(hail1, hail2): hail1.mht_distance(hail2) for hail1, hail2 in combinations(hails, 2)}
    
    min_haildistance = min([(h1, h2, d) for (h1, h2), d in hail_distances.items()], key=lambda x: x[2])
    
    min_hail1, min_hail2, _ = min_haildistance
    next_min_haildistances = {k: v for k, v in hail_distances.items() if k[0] == min_hail1 and k[1] != min_hail2}
    min_haildistance2 = min([(h1, h2, d) for (h1, h2), d in next_min_haildistances.items()], key=lambda x: x[2])
    
    min_hail3 = min_haildistance2[1]
    
    print(min_haildistance, min_hail3)
    
    # (x2 - x1 + vx2*t2 - vx1*t1)(t3-t1) = (x3 - x1 + vx3*t3 - vx1*t1)(t2-t1)
    # (y2 - y1 + vy2*t2 - vy1*t1)(t3-t1) = (y3 - y1 + vy3*t3 - vy1*t1)(t2-t1)
    # (z2 - y1 + vz2*t2 - vz1*t1)(t3-t1) = (z3 - z1 + vz3*t3 - vz1*t1)(t2-t1)
    
    #1 (x2-x1)t3 + (x3-x2)t1 - (x3-x1)t2 + (vx2-vx3)*t2*t3 + (vx3 - vx1)*t1*t3 +(vx1-vx2)*t2*t1 = 0
    #2 (y2-y1)t3 + (y3-y2)t1 - (y3-y1)t2 + (vy2-vy3)*t2*t3 + (vy3 - vy1)*t1*t3 +(vy1-vy2)*t2*t1 = 0
    #3 (z2-z1)t3 + (z3-z2)t1 - (z3-z1)t2 + (vz2-vz3)*t2*t3 + (vz3 - vz1)*t1*t3 +(vz1-vz2)*t2*t1 = 0
    
    # a1t1 + b1t2 + c1t3 + d1t1t2 + e1t2t3 + f1t1t3 = 0 
    # a2t1 + b2t2 + c2t3 + d2t1t2 + e2t2t3 + f2t1t3 = 0 
    # a3t1 + b3t2 + c3t3 + d3t1t2 + e3t2t3 + f3t1t3 = 0 
    
    #1 t2 = -(a1t1 + c1t3 + f1t1t3)/(b1 + d1t1 + e1t3)
    #2 t2 = -(a2t1 + c2t3 + f2t1t3)/(b2 + d2t1 +e2t3)
    #3 t2 = -(a3t1+c3t3+f3t1t3)/(b3+d3t1+e3t3)
    
    #1 & 2   (a1t1 + c1t3 + f1t1t3)*(b2+d2t1+e2t3) = (a2t1 + c2t3 + f2t1t3)*(b1 + d1t1 + e1t3)
    # a1*t1*b2 + a1*d2*t1**2 + a1*e2*t1*t3 + c1*b2*t3 + c1*d2*t1*t3 + c1*e2*t3**2 + f1*b2*t1*t3 + f1*d2*t3*t1**2 + f1*e2*t1*t3**2 =
    #     a2*b1*t1 + a2*d1*t1**2 + a2*e1*t1*t3 + c2*b1*t3 + c2*d1*t1*t3 + c2*e1*t3**2 + f2*b1*t1*t3 + f2*d1*t3*t1**2 + f2*e1*t1*t3**2
    
    # (a1*b2 + a1*e2*t3 + c1*d2*t3 + f1*b2*t3 + f1*e2*t3**2 - a2*b1 - a2*e1*t3 - c2*d1*t3 - f2*b1*t3 - f2*e1*t3**2)*t1 +
    #        (a1*d2 + f1*d2*t3 - a2*d1 - f2*d1*t3)*t1**2 + c1*b2*t3 + c1*e2*t3**2 - c2*b1*t3 - c2*e1*t3**2 = 0
    
    x1 = min_hail1.position.x;  y1 = min_hail1.position.y; z1 = min_hail1.position.z
    x2 = min_hail2.position.x;  y2 = min_hail2.position.y; z2 = min_hail2.position.z
    x3 = min_hail3.position.x;  y3 = min_hail3.position.y; z3 = min_hail3.position.z
    
    vx1 = min_hail1.velocity.x; vy1 = min_hail1.velocity.y; vz1 = min_hail1.velocity.z
    vx2 = min_hail2.velocity.x; vy2 = min_hail2.velocity.y; vz2 = min_hail2.velocity.z
    vx3 = min_hail3.velocity.x; vy3 = min_hail3.velocity.y; vz3 = min_hail3.velocity.z
    
    a1 = x3-x2;b1 = x1-x3; c1=x2-x1; d1 = vx1-vx2; e1 = vx2-vx3; f1 = vx3-vx1
    a2 = y3-y2;b2 = y1-y3; c2=y2-y1; d2 = vy1-vy2; e2 = vy2-vy3; f2 = vy3-vy1
    a3 = z3-z2;b3 = z1-z3; c3=z2-z1; d3 = vz1-vz2; e3 = vz2-vz3; f3 = vz3-vz1
    
    t3 = 0
    while True:
        t3 += 1
        if set(str(t3)[1:]) == {'0'}:
            print(t3)
            
        a = (a1*d2 + f1*d2*t3 - a2*d1 - f2*d1*t3)
        b = (a1*b2 + a1*e2*t3 + c1*d2*t3 + f1*b2*t3 + f1*e2*t3**2 - a2*b1 - a2*e1*t3 - c2*d1*t3 - f2*b1*t3 - f2*e1*t3**2)
        c = c1*b2*t3 + c1*e2*t3**2 - c2*b1*t3 - c2*e1*t3**2 
        
        t1 = None
        if a == 0:
            t1_1 = -c/b
            if t1_1 == int(t1_1) and t1_1 != t3 and t1_1 > 0:
                t1 = int(t1_1)
        else:
            delta = b**2 - 4*a*c
            
            t1_1 = (-b + sqrt(delta))/(2*a)
            t1_2 = (-b - sqrt(delta))/(2*a)
            
            if t1_1 == int(t1_1) and t1_1 != t3 and t1_1 > 0:
                if t1_2 == int(t1_2) and t1_2 != t3 and t1_2 > 0:
                    print(f'There are 2 posible values for t1 {t1_1} and {t1_2}')
                t1 = int(t1_1)
            elif t1_2 == int(t1_2) and t1_2 != t3 and t1_2 > 0:
                t1 = int(t1_2)
            
        t2 = None
        if t1: # test with t2
            t2_1 = -(a1*t1 + c1*t3 + f1*t1*t3)/(b1 + d1*t1 + e1*t3)
            if t2_1 == int(t2_1) and t2_1 != t1 and t2_1 != t3 and t2_1 > 0:
                t2_2 = -(a2*t1 + c2*t3 + f2*t1*t3)/(b2 + d2*t1 +e2*t3)
                if t2_2 == t2_1:
                    t2_3 = -(a3*t1 + c3*t3 + f3*t1*t3)/(b3 + d3*t1 + e3*t3)
                    if t2_3 == t2_2:
                        t2 = int(t2_1)
        if t2:
            break
    
    print('ts', t1, t2, t3)
    
    hx1 = vx1*t1 + x1; hy1 = vy1*t1 + y1; hz1 = vz1*t1 + z1
    hx2 = vx2*t2 + x2; hy2 = vy2*t2 + y2; hz2 = vz2*t2 + z2
    
    dt21 = t2 - t1
    vsx = (hx2 - hx1)/dt21; vsy = (hy2 - hy1)/dt21; vsz = (hz2 - hz1)/dt21
    
    sx = hx1 - vsx*t1; sy = hy1 - vsy*t1; sz = hz1 - vsz*t1
    return sx + sy + sz
    
@session.submit_result(level=2, tests=[({'inp': [
    '19, 13, 30 @ -2,  1, -2',
    '18, 19, 22 @ -1, -1, -2',
    '20, 25, 34 @ -2, -2, -4',
    '12, 31, 28 @ -1, -2, -1',
    '20, 19, 15 @  1, -5, -3'
]}, 47)], wrong_answers={
    769281292688186, #too low
})
def solve_part2(inp: list[str]) -> int:
    hails = [Hailstone2.parse_line(line) for line in inp]
    hail1, hail2, hail3, *_ = hails
    
    y1 = (hail1.position @ hail1.velocity) - (hail2.position @ hail2.velocity)
    y2 = (hail1.position @ hail1. velocity) - (hail3.position @ hail3.velocity)
    
    yl = [y1.x, y1.y, y1.z, y2.x, y2.y, y2.z]
    
    mat_a = np.array([
        [0, hail1.velocity.z - hail2.velocity.z, hail2.velocity.y - hail1.velocity.y, 0, hail1.position.z - hail2.position.z, hail2.position.y - hail1.position.y],
        [hail2.velocity.z - hail1.velocity.z, 0, hail1.velocity.x - hail2.velocity.x, hail2.position.z - hail1.position.z, 0, hail1.position.x - hail2.position.x],
        [hail1.velocity.y - hail2.velocity.y, hail2.velocity.x - hail1.velocity.x, 0, hail1.position.y - hail2.position.y, hail2.position.x - hail1.position.x, 0],
        [0, hail1.velocity.z - hail3.velocity.z, hail3.velocity.y - hail1.velocity.y, 0, hail1.position.z - hail3.position.z, hail3.position.y - hail1.position.y],
        [hail3.velocity.z - hail1.velocity.z, 0, hail1.velocity.x - hail3.velocity.x, hail3.position.z - hail1.position.z, 0, hail1.position.x - hail3.position.x],
        [hail1.velocity.y - hail3.velocity.y, hail3.velocity.x - hail1.velocity.x, 0, hail1.position.y - hail3.position.y, hail3.position.x - hail1.position.x, 0]
    ])
    
    inv_mat_a = np.linalg.inv(mat_a)
    inva = [list(row) for row in inv_mat_a]
    
    x_stone = sum([a*b for a, b in zip(yl, inva[0])])
    y_stone = sum([a*b for a, b in zip(yl, inva[1])])
    z_stone = sum([a*b for a, b in zip(yl, inva[2])])
    return round(x_stone + y_stone + z_stone) 


if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
