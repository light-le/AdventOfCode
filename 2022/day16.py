from typing import Dict, Tuple
from functools import reduce
from collections import deque, namedtuple, defaultdict
from utils import AdventSession, extract_year_day_from_path
from functools import cached_property
from itertools import combinations_with_replacement, product
from pprint import pprint
from datetime import datetime
session = AdventSession(**extract_year_day_from_path(__file__))

class Valve:
    def __init__(self, name: str, rate: int) -> None:
        self.name = name
        self.flow_rate = rate
        self.connected_valves = set()
        self.is_open = None
        
    def copy(self):
        new_valve = self.__class__(self.name, self.flow_rate)
        new_valve.connected_valves = self.connected_valves
        new_valve.is_open = self.is_open
        return new_valve
        
    def __hash__(self) -> int:
        return hash(self.name)
    
    def __eq__(self, __o: object) -> bool:
        return self.name == __o.name
        
    def connect(self, valve: object) -> None:
        self.connected_valves.add(valve.name)
        valve.connected_valves.add(self.name)
        
    def __repr__(self) -> str:
        return f'{self.is_open}'
        # return (f'Valve {self.name} with rate {self.flow_rate} is connected to '
        #         f'{[valve.name for valve in self.connected_valves]}')
        
    def estimate_points_at(self, minutes: int) -> int:
        return self.flow_rate*minutes
    
    @cached_property
    def steps_to_all_valves(self) -> Dict:
        '''
        BFS to get the least number of step to all valves
        '''
        frontier = deque([self])
        current_step = 0
        all_valve_steps = {
            self: current_step
        }
        while frontier:
            current_valve = frontier.popleft()
            current_step = all_valve_steps[current_valve] + 1
            next_valves = [valve for valve in current_valve.connected_valves if valve not in all_valve_steps]
            all_valve_steps.update({next_valve: current_step for next_valve in next_valves})
            frontier.extend(next_valves)
        return all_valve_steps
            
            
            
        
        
    @classmethod
    def parse_valve(cls, line: str, all_valves: Dict) -> object:
        
        flow_rate, connections = line.split('; ')
        valve_flow, rate = flow_rate.split('=')
        val, name, *_ = valve_flow.split(' ')
        
        valve = cls(name, int(rate))
        all_valves[name] = valve

        tunnel, lead, to, val, *valves = connections.split(' ')
        connected_names = [valve.replace(',', '') for valve in valves]

        for connected_name in connected_names:
            if connected_name in all_valves:
                valve.connect(all_valves[connected_name])
        return valve

State = namedtuple('State', ['points', 'valves'])

def fill_none_or_max(old_state: State, new_state):
    if old_state is None:
        return new_state
    if old_state.points < new_state.points:
        return new_state
    return old_state

@session.submit_result(level=1, tests=[({'inp': [
    'Valve AA has flow rate=0; tunnels lead to valves DD, II, BB',
    'Valve BB has flow rate=13; tunnels lead to valves CC, AA',
    'Valve CC has flow rate=2; tunnels lead to valves DD, BB',
    'Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE',
    'Valve EE has flow rate=3; tunnels lead to valves FF, DD',
    'Valve FF has flow rate=0; tunnels lead to valves EE, GG',
    'Valve GG has flow rate=0; tunnels lead to valves FF, HH',
    'Valve HH has flow rate=22; tunnel leads to valve GG',
    'Valve II has flow rate=0; tunnels lead to valves AA, JJ',
    'Valve JJ has flow rate=21; tunnel leads to valve II'
]}, 1651)]
)
def solve_part1(inp):
    all_valves = dict()
    valves = [Valve.parse_valve(line, all_valves) for line in inp]
    
    minute = 30
    
    all_states = {
        minute: {
            valve.name: dict() for valve in valves
        } for minute in range(minute)
    }
    
    next_valves = [('AA', {valve_name: valve.copy() for valve_name, valve in all_valves.items()}, 0)]
    
    while minute > 0:
        minute -= 1
        for next_valve_name, all_valves, current_points in next_valves:
            next_valve = all_valves[next_valve_name]
            opened_valve_names = tuple(sorted([valve_name for valve_name, valve in all_valves.items() if valve.is_open]))
            for next_connected_valve_name in next_valve.connected_valves:
                # choose to move to next
                all_states[minute][next_connected_valve_name][opened_valve_names] = fill_none_or_max(
                    all_states[minute][next_connected_valve_name].get(opened_valve_names),
                    State(current_points, {valve_name: valve.copy() for valve_name, valve in all_valves.items()})
                )
            
            if next_valve.flow_rate > 0 and next_valve.is_open is None:
                # choose to open
                all_valves_copy = {valve_name: valve.copy() for valve_name, valve in all_valves.items()}
                next_valve = all_valves_copy[next_valve_name]
            
                points = next_valve.estimate_points_at(minute) + current_points
                next_valve.is_open = minute
                opened_valve_names = tuple(sorted([valve_name for valve_name, valve in all_valves_copy.items() if valve.is_open]))
                all_states[minute][next_valve_name][opened_valve_names] = fill_none_or_max(all_states[minute][next_valve_name].get(opened_valve_names),
                                                                                           State(points, all_valves_copy))
                
        available_state_dicts = [
            (valve_name, state_dict) for valve_name, state_dict in all_states[minute].items()
            if state_dict
        ]
        next_valves = list()
        for valname, state_dict in available_state_dicts:
            for opened, state in state_dict.items():
                next_valves.append((valname, state.valves, state.points))
        
        print('minute', minute)
    last_state_result = all_states[0]
    
    last_states = list()
    for valname, state_dict in last_state_result.items():
        last_states.extend(list(state_dict.values()))
    
    return max([state.points for state in last_states]) # 1987 too low
    
def add_str_to_sorted_tuple(sorted_tuple: Tuple, name: str) -> Tuple:
    if not sorted_tuple:
        return (name,)  
    for i, item in enumerate(sorted_tuple):
        if item > name:
            return (*sorted_tuple[:i], name, *sorted_tuple[i:])
    return sorted_tuple + (name,)

@session.submit_result(level=2, tests=[({'inp': [
    'Valve AA has flow rate=0; tunnels lead to valves DD, II, BB',
    'Valve BB has flow rate=13; tunnels lead to valves CC, AA',
    'Valve CC has flow rate=2; tunnels lead to valves DD, BB',
    'Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE',
    'Valve EE has flow rate=3; tunnels lead to valves FF, DD',
    'Valve FF has flow rate=0; tunnels lead to valves EE, GG',
    'Valve GG has flow rate=0; tunnels lead to valves FF, HH',
    'Valve HH has flow rate=22; tunnel leads to valve GG',
    'Valve II has flow rate=0; tunnels lead to valves AA, JJ',
    'Valve JJ has flow rate=21; tunnel leads to valve II'
]}, 1707)])
def solve_part2(inp):
    all_valves = dict()
    valves = [Valve.parse_valve(line, all_valves) for line in inp]
    
    minute = 26
    
    # last_states = defaultdict(lambda: defaultdict(int))
    next_valves = [('AA', 'AA', tuple(), 0)]
    elapsed = datetime.now()
    while minute > 0:
        minute -= 1
        next_states = defaultdict(lambda: defaultdict(int))

        for your_next_valname, e_next_valname, sorted_open_valnames, current_points in next_valves:
            if your_next_valname == e_next_valname:
                for your_e_next_val in combinations_with_replacement(all_valves[your_next_valname].connected_valves, 2):
                    # choose to move to next, for you
                    next_states[sorted_open_valnames][your_e_next_val] = max(next_states[sorted_open_valnames][your_e_next_val], current_points)
            else:
                for your_next_conname, e_next_conname in product(all_valves[your_next_valname].connected_valves,
                                                                 all_valves[e_next_valname].connected_valves):
                    your_e_next_val = (your_next_conname, e_next_conname)
                    next_states[sorted_open_valnames][your_e_next_val] = max(next_states[sorted_open_valnames][your_e_next_val], current_points)
            
            if all_valves[your_next_valname].flow_rate > 0 and your_next_valname not in sorted_open_valnames:
                # choose to open
                your_next_open_valve = all_valves[your_next_valname]
            
                your_points = your_next_open_valve.estimate_points_at(minute) + current_points
                your_open_valnames = add_str_to_sorted_tuple(sorted_open_valnames, your_next_valname)
                
                for e_next_conname in all_valves[e_next_valname].connected_valves:
                    your_e_next_val = (your_next_valname, e_next_conname)
                    next_states[your_open_valnames][your_e_next_val] = max(next_states[your_open_valnames][your_e_next_val], your_points)
                    
            if all_valves[e_next_valname].flow_rate > 0 and e_next_valname not in sorted_open_valnames:
                e_next_open_valve = all_valves[e_next_valname]
                
                e_points = e_next_open_valve.estimate_points_at(minute) + current_points
                e_open_valnames = add_str_to_sorted_tuple(sorted_open_valnames, e_next_valname)

                for your_next_conname in all_valves[your_next_valname].connected_valves:
                    your_e_next_val = (your_next_conname, e_next_valname)
                    next_states[e_open_valnames][your_e_next_val] = max(next_states[e_open_valnames][your_e_next_val], e_points)
                    
            if (all_valves[your_next_valname].flow_rate > 0 and your_next_valname not in sorted_open_valnames and
                all_valves[e_next_valname].flow_rate > 0 and e_next_valname not in sorted_open_valnames and
                your_next_valname != e_next_valname):
                your_e_open_valnames = add_str_to_sorted_tuple(e_open_valnames, your_next_valname)
                your_e_next_val = (your_next_valname, e_next_valname)
                
                your_e_points = your_points + e_points - current_points
                next_states[your_e_open_valnames][your_e_next_val] = max(next_states[your_e_open_valnames][your_e_next_val], your_e_points)

        next_valves = list()
        for open_valnames, current_valves_points in next_states.items():
            for (your_current_valve, e_current_valve), points in current_valves_points.items():
                next_valves.append((your_current_valve, e_current_valve, open_valnames, points))
        
        print('minute', minute, 'elapsed ', (datetime.now() - elapsed).seconds)
        elapsed = datetime.now()
        
        # last_states = next_states
    
    all_points = list()
    for open_valnames, current_valves_points in next_states.items():
        for current_valves, points in current_valves_points.items():
            all_points.append(points)
            
    return max(all_points)
    
if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
