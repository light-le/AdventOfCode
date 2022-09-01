
from abc import abstractmethod
from collections import deque
from enum import Enum
from itertools import combinations
from typing import Dict, Iterable, List, Set, Tuple
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class Directions(Enum):
    UP = 1
    DOWN = -1

class AbstractChip:
    def __init__(self, rad: str) -> None:
        self.radioactive = rad
        
    def __repr__(self) -> str:
        return f'{self.radioactive} {str(self.__class__)}'
    
    @abstractmethod
    def can_be_fried(self, __o) -> bool:
        return False
        
class Microchip(AbstractChip):
    def can_be_fried(self, __o: AbstractChip) -> bool:
        if isinstance(__o, Generator) and __o.radioactive != self.radioactive:
            return True
        return False

class Generator(AbstractChip):
    pass

def parse_chip_generator(txt: str) -> AbstractChip:
    type, device = txt.split(' ')
    if device == 'generator':
        return Generator(type)
    elif device == 'microchip':
        return Microchip(type)
    else:
        raise Exception(f'Invalid device {device}')
    
def parse_floor(txt: str) -> int:
    if 'first' in txt:
        return 1
    elif 'second' in txt:
        return 2
    elif 'third' in txt:
        return 3
    elif 'fourth' in txt:
        return 4
    else:
        raise Exception(f'Invalid floor {txt}')

def parse_input(txt: str) -> Tuple[int, Set]:
    floor, containees = txt.split(' contains ')
    floor_no = parse_floor(floor)
    
    clean_containees = (containees.replace('a ', '').replace('and ', '')
                                  .replace('-compatible', '').replace('.', ''))
    if clean_containees == 'nothing relevant':
        return floor_no, set()
    
    chip_gens = {parse_chip_generator(con) for con in clean_containees.split(', ')}
    return floor_no, chip_gens
    
class State:
    '''
    A state is the current 'state' of the move. It has floor map, current floor
    '''
    def __init__(self, floor_map: Dict, current_floor: int, step: int=0) -> None:
        self.floor_map = {floor_no: frozenset(devices) for floor_no, devices in floor_map.items()}
        self.current_floor = current_floor
        self.step = step
        
    def __hash__(self) -> int:
        return hash((frozenset(self.floor_map), self.current_floor))
    
    def count_devices(self, type: AbstractChip=Generator) -> Dict:
        return {floor: len([device for device in self.floor_map[floor]
                            if isinstance(device, type)])
                for floor in self.floor_map}
    
    
    def __eq__(self, __o: object) -> bool:
        '''
        Old way - hard check - states are the same if floor_map is exactly the same
        return (all([self.floor_map[floor] == __o.floor_map[floor] for floor in self.floor_map]) and
                self.current_floor == __o.current_floor)
        New way - soft check - states are the same if same number of chips, gens at each floor
        '''
        return (self.current_floor == __o.current_floor and
                self.count_devices(Generator) == __o.count_devices(Generator) and
                self.count_devices(Microchip) == __o.count_devices(Microchip))
        
    
    def check_floor(self, floor: int=None) -> bool:
        '''
        Check if there's a chip left alone with another RTG
        '''
        floor = floor or self.current_floor
        floor_devices = self.floor_map[floor]
        
        generators = {device for device in floor_devices if isinstance(device, Generator)}
        microchips = {device for device in floor_devices if isinstance(device, Microchip)}
        
        if generators and microchips:
            for microchip in microchips:
                if not any({gen.radioactive == microchip.radioactive for gen in generators}):
                    return False
        return True
    
    @property
    def current_device(self):
        return self.floor_map[self.current_floor]
    
    def new_state(self, devices: Tuple[AbstractChip, ...], dir: Directions=Directions.UP) -> object:
        '''
        given a device carried from current floor to next, produce new state if floor checks out
        '''
        remaining_devices = {device for device in self.current_device if device not in devices}
        next_floor_n = self.current_floor+dir.value
        next_floor_devices = self.floor_map[next_floor_n] | set(devices)
        
        new_state = State(floor_map={**self.floor_map,
                                     **{next_floor_n: next_floor_devices,
                                        self.current_floor: remaining_devices}},
                          current_floor=next_floor_n,
                          step=self.step+1)
        
        if new_state.check_floor(self.current_floor) and new_state.check_floor():
            return new_state
        
    @staticmethod
    def find_generators_microchip_pairs(gens: Iterable[Generator], chips: Iterable[Microchip]
                                        ) -> Tuple[Generator, Microchip]:
        for gen in gens:
            for chip in chips:
                if gen.radioactive == chip.radioactive:
                    return gen, chip
                
    @staticmethod
    def find_standalone_generators(gens: Iterable[Generator], chips: Iterable[Microchip]
                                   ) -> Tuple[Generator, ...]:
        chip_radioactives = {chip.radioactive for chip in chips}
        standalone_gens = [gen for gen in gens if gen.radioactive not in chip_radioactives]
        return tuple(standalone_gens[:2])
    
    @staticmethod
    def pick_2_or_1_from(genchips: Iterable[AbstractChip]) -> Tuple[AbstractChip, ...]:
        picks = set()
        while genchips and len(picks) < 2:
            picks.add(genchips.pop())
        return tuple(picks)
    
    def derive_combinations(self) -> List:
        pair_combination = list(combinations(self.current_device, 2))
        single_combination = [(device, ) for device in self.current_device]
        all_combinations = pair_combination + single_combination
        
        dir_combs = list()
        
        if self.current_floor < 4:
            dir_combs.extend([(Directions.UP, comb) for comb in all_combinations])
        if self.current_floor > 1 and any([
                len(self.floor_map[floor]) > 0 for floor in range(1, self.current_floor)]):
            dir_combs.extend([(Directions.DOWN, (chip, )) for chip in self.current_device])
            
        return dir_combs
    
    def is_complete(self) -> bool:
        return all([len(self.floor_map[floor]) == 0 for floor in range(1, 4)])
    
    def __repr__(self) -> str:
        return f'{self.floor_map} {self.current_floor}'
    
    @property
    def score(self) -> int:
        return sum([len(self.floor_map[floor])*floor for floor in self.floor_map])

def solve_parts(floor_map: Dict) -> int:
    initstate = State(floor_map, 1)
    
    frontier = deque([initstate])
    visited_states = {initstate}
    
    answer = None
    while frontier and answer is None:
        state = frontier.popleft()
        combinations = state.derive_combinations()
        for direction, combination in combinations:
            new_state = state.new_state(combination, direction)
            if new_state and new_state.is_complete():
                answer = new_state.step
                break
            
            if new_state and new_state not in visited_states:
                fourth_len = len(new_state.floor_map[4])

                frontier.append(new_state)
                visited_states.add(new_state)
    return answer


@session.submit_result(level=1, tests=[({'floor_map': {
    1: {Microchip('H'), Microchip('L')},
    2: {Generator('H')},
    3: {Generator('L')},
    4: set()
}}, 11)])
def solve_part1(floor_map: Dict):
    return solve_parts(floor_map)
    
    

@session.submit_result(level=2)
def solve_part2(floor_map):
    floor_map[1] |= {Generator('elerium'), Microchip('elerium'), 
                     Generator('dilithium'), Microchip('dilithium')}
    return solve_parts(floor_map)


if __name__ == '__main__':
    inp = [i for i in session.read_input().split('\n') if i]
    floor_maps = dict()
    
    for txt in inp:
        floor_no, chip_gens = parse_input(txt)
        floor_maps[floor_no] = chip_gens
        
    solve_part1(floor_maps)
    
    solve_part2(floor_maps)
