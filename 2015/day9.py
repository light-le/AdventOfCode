from functools import cache
from itertools import permutations
from typing import Dict, Tuple
from utils import AdventSession, extract_year_day_from_path
from dataclasses import dataclass

class Map:
    '''A map is a full travel plan through all points in a certain order
    all_maps should hold all possible maps, without the ones in reverse
    For example it should have ABC (not CBA), ACB (not BCA), BAC (not CAB)'''
    all_maps = set()
    def __init__(self, points: Tuple) -> None:
        self.points = points
        if points[::-1] not in self.all_maps:
            self.all_maps.add(points)

    @staticmethod
    def evaluate_distance(map: Tuple, distance_book: Dict) -> int:
        total_distance = 0
        for p in range(len(map)-1):
            total_distance += distance_book[(map[p], map[p+1])]
        return total_distance

@dataclass
class Route:
    '''A route is a way from point A to point B with distance in between'''
    start: str
    end: str
    distance: int

    points = set()
    all_routes = dict()
    def __post_init__(self):
        cls = self.__class__

        cls.points.add(self.start)
        cls.points.add(self.end)

        cls.all_routes[(self.start, self.end)] = self.distance
        cls.all_routes[(self.end, self.start)] = self.distance

    @classmethod
    def parse_route(cls, route: str):
        places, dist = route.split(' = ')
        start, end = places.split(' to ')
        return cls(start=start, end=end, distance=int(dist))

@cache
def brute_force_all_distances():
    permute_points = permutations(Route.points, len(Route.points))
    maps = [Map(map) for map in permute_points]

    distances = [Map.evaluate_distance(map, Route.all_routes) for map in Map.all_maps]
    return distances


if __name__ == '__main__':
    session = AdventSession(**extract_year_day_from_path(__file__))
    routes = [Route.parse_route(route) for route in session.read_input().split('\n') if route]

    distances = brute_force_all_distances()

    part1_answer = min(distances)
    print(part1_answer)
    session.post_answer(part1_answer, level=1)

    part2_answer = max(distances)
    print(part2_answer)
    session.post_answer(part2_answer, level=2)

    

