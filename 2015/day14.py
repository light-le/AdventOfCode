from dataclasses import dataclass
from utils import AdventSession, extract_year_day_from_path

@dataclass
class Reindeer:
    name: str
    speed: int
    stamina: int
    rest: int
    
    def __post_init__(self):
        self.distance_per_interval = self.speed*self.stamina
        self.interval = self.stamina + self.rest
        self.points = 0
        
    def get_position(self, at: int) -> int:
        n_intervals = at // self.interval
        distance_at_n_intervals = self.distance_per_interval*n_intervals
        
        remaining_seconds = at % self.interval
        distance_travelled_in_remaining = min(remaining_seconds, self.stamina) * self.speed
        return distance_at_n_intervals + distance_travelled_in_remaining
    
    def accumulate_distance(self, sec:int=0) -> int:
        if sec == 0:
            self.state = 'running'
            self.state_duration = 1
            self.distance = self.speed
        else:
            if self.state == 'running':
                if self.state_duration < self.stamina:
                    self.distance += self.speed
                    self.state_duration+=1
                else:
                    self.state = 'rest'
                    self.state_duration = 1
            else:
                if self.state_duration < self.rest:
                    self.state_duration+=1
                else:
                    self.state = 'running'
                    self.distance += self.speed
                    self.state_duration = 1
                    
    def bonus_point(self):
        self.points+=1
        
        
    
    @classmethod
    def parse_deer_text(cls, txt: str):
        name, can, fly, speed, unit, four, stamina, *_, rest, sec = txt.split(' ')
        return cls(name, int(speed), int(stamina), int(rest))

def solve_part1(deers):
    positions = [deer.get_position(at=2503) for deer in deers]
    return max(positions)

def solve_part2(deers):
    for sec in range(2503):
        [deer.accumulate_distance(sec) for deer in deers]
        max_distance = max(deer.distance for deer in deers)
        [deer.bonus_point() for deer in deers if deer.distance == max_distance]
    return max(deer.points for deer in deers)
        
        

if __name__ == "__main__":
    session = AdventSession(**extract_year_day_from_path(__file__))
    
    speedstr = [s for s in session.read_input().split('\n') if s]
    deers = [Reindeer.parse_deer_text(ss) for ss in speedstr]
    
    part1_answer = solve_part1(deers)
    print(part1_answer)
    session.post_answer(part1_answer, level=1)
    
    part2_answer = solve_part2(deers)
    print(part2_answer)
    session.post_answer(part2_answer, level=2)
    
    