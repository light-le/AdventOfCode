from copy import deepcopy
class Vertice:
    def __init__(self, row, col, risk) -> None:
        self.row = row
        self.col = col
        self.risk = risk

        self._shortest_total_risk = 0 if (row == 0 and col == 0) else float("Inf")
        self.adjacents = []

    def __repr__(self) -> str:
        return f'{self.row} {self.col} {self.risk}'

    @property
    def shortest_total_risk(self):
        return self._shortest_total_risk

    @shortest_total_risk.setter
    def shortest_total_risk(self, str):
        self._shortest_total_risk = str
        for adjacent in self.adjacents:
            if adjacent.shortest_total_risk > (str+adjacent.risk) and adjacent.shortest_total_risk != float("Inf"):
                adjacent.shortest_total_risk = str + adjacent.risk

def part1_solution(rm):
    for row in rm:
        for vertice in row:
            for adjacent in vertice.adjacents:
                total_risk = vertice.shortest_total_risk + adjacent.risk
                if total_risk < adjacent.shortest_total_risk:
                    adjacent.shortest_total_risk = total_risk
    return rm[-1][-1].shortest_total_risk


def convert_value_to_vertice(risk_map):
    for r, row in enumerate(risk_map):
        for c, risk in enumerate(row):
            vertice = Vertice(r, c, risk)
            if c > 0:
                vertice.adjacents.append(risk_map[r][c-1]) # left
                risk_map[r][c-1].adjacents.append(vertice)
            if r > 0:
                vertice.adjacents.append(risk_map[r-1][c]) # up above
                risk_map[r-1][c].adjacents.append(vertice)
            risk_map[r][c] = vertice
    return risk_map

def map_increment(map, by=1):
    return [[(c+by)%9 if (c+by)%9 else 9 for c in row] for row in map]

def attach_hor(map_list):
    big_map = []
    for r in range(len(map_list[0])):
        big_row = []
        for map in map_list:
            big_row.extend(map[r])
        big_map.append(big_row)
    return big_map

if __name__ == "__main__":
    with open('2021/day15.txt', 'r') as f:
        map = f.read().rsplit()
        risk_map = [[int(c) for c in row] for row in map]
    
    rm = convert_value_to_vertice(deepcopy(risk_map))
    print(part1_solution(rm))

    map_increments = [map_increment(risk_map, by) for by in range(9)]
    big_map = attach_hor(map_increments[:5]) + \
            attach_hor(map_increments[1:6]) + \
            attach_hor(map_increments[2:7]) + \
            attach_hor(map_increments[3:8]) + \
            attach_hor(map_increments[4:9])
    brm = convert_value_to_vertice(deepcopy(big_map))
    print(part1_solution(brm))