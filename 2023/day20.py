from __future__ import annotations
from enum import Enum
from math import lcm
from abc import abstractmethod
from collections import namedtuple, deque
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

Pulse = namedtuple('Pulse', ['origin', 'magnitude', 'destination'])

class PulseMagnitude(Enum):
    HIGH = 1
    LOW = -1

class Pulser:
    '''Base class of all type, can send high/low pulse to targets'''
    # ALL_PULSERS = dict()
    # PULSES_COUNT = {
    #     PulseMagnitude.HIGH: 0,
    #     PulseMagnitude.LOW: 0
    # }
    
    @classmethod
    def reset(cls):
        cls.ALL_PULSERS = dict()
        cls.PULSES_COUNT = {
            PulseMagnitude.HIGH: 0,
            PulseMagnitude.LOW: 0
        }

    def __init__(self, name: str, targets: list[Pulser]=None) -> None:
        self.name = name
        self.targets = targets or list()

        self.__class__.ALL_PULSERS[name] = self
        
    def send_pulses(self, magnitude: PulseMagnitude) -> list[Pulse]:
        self.__class__.PULSES_COUNT[magnitude] += len(self.targets)
        return [Pulse(self, magnitude, target) for target in self.targets]
    
    def add_targets(self, targets: list[Pulser]) -> None:
        self.targets.extend(targets)
    
    def add_target(self, target: Pulse) -> None:
        self.targets.append(target)
        
    def __repr__(self) -> str:
        return self.name
    
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name
    
    @abstractmethod
    def trigger(self, pulse: Pulse):
        return []
    
class Button(Pulser):
    '''A button can only send low pulse to the broadcaster upon pushing'''
    def __init__(self) -> None:
        super().__init__('button', targets=[self.__class__.ALL_PULSERS['broadcaster']])
        
    def trigger(self) -> list[Pulse]:
        return self.send_pulses(magnitude=PulseMagnitude.LOW)
    
class Broadcaster(Pulser):
    '''A broadcaster send the same kind of pulses to all targets'''
    def trigger(self, pulse: Pulse) -> list[Pulse]:
        return self.send_pulses(pulse.magnitude)
    
class FlipFlop(Pulser):
    '''A FlipFlop is a Pulser with state (on or off, True of False). Initially off'''
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.on = False
        
    def trigger(self, pulse: Pulse) -> list[Pulse]:
        if pulse.magnitude == PulseMagnitude.HIGH:
            return []
        elif pulse.magnitude == PulseMagnitude.LOW:
            pulse_mag = PulseMagnitude.LOW if self.on else PulseMagnitude.HIGH
            self.on = not self.on
            return self.send_pulses(pulse_mag)
        else:
            raise Exception(f'Invalid pulse input {pulse}')
        
class Conjunction(Pulser):
    '''A conjunction pulser remember the type of the most recent pulse received
    from each of their connected input modules; 
    they initially default to remembering a low pulse for each input.'''
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.pulse_inputs = dict()
        
    def init_pulse_input(self, input_pulse_name: str) -> None:
        self.pulse_inputs.update({input_pulse_name: PulseMagnitude.LOW})
        
    def trigger(self, pulse: Pulse):
        self.pulse_inputs[pulse.origin.name] = pulse.magnitude
        pulse_mag = PulseMagnitude.LOW if all([pv == PulseMagnitude.HIGH for pv in self.pulse_inputs.values()]) else PulseMagnitude.HIGH
        return self.send_pulses(pulse_mag)
                
@session.submit_result(level=1, tests=[({'inp': [
    'broadcaster -> a, b, c',
    '%a -> b',
    '%b -> c',
    '%c -> inv',
    '&inv -> a'
]}, 32000000), ({'inp': [
    'broadcaster -> a',
    '%a -> inv, con',
    '&inv -> b',
    '%b -> con',
    '&con -> output'
]}, 11687500)])
def solve_part1(inp: list[str]):
    button = parse_modules(inp)
    
    for button_push in range(1000):
        frontier = deque(button.trigger())
        
        while frontier:
            pulse = frontier.popleft()
            frontier.extend(pulse.destination.trigger(pulse))
    return Pulser.PULSES_COUNT[PulseMagnitude.HIGH] * Pulser.PULSES_COUNT[PulseMagnitude.LOW]

def parse_modules(inp):
    Pulser.reset()
    source_target_str = dict()
    for line in inp:
        source, target = line.split(' -> ')
        target_str = target.split(', ')
        if source == 'broadcaster':
            Broadcaster(source)
        elif source.startswith("%"):
            FlipFlop(source[1:])
        elif source.startswith("&"):
            Conjunction(source[1:])
        else:
            raise Exception(f'Invalid source {source}')
        
        source_target_str[source.replace("%", "").replace("&", "")] = target_str
        
    button = Button()
    for source, target_l in source_target_str.items():
        for t in target_l:
            if t in Pulser.ALL_PULSERS:
                target_pulse = Pulser.ALL_PULSERS[t]
            else:
                target_pulse = Pulser(t)
            Pulser.ALL_PULSERS[source].add_target(target_pulse)
            if isinstance(target_pulse, Conjunction):
                target_pulse.init_pulse_input(source)
    return button
            
@session.submit_result(level=2)
def solve_part2(inp: list[str]):
    button = parse_modules(inp)
    button_pushes = 0
    
    conjunction_b4_final = Pulser.ALL_PULSERS['kl'] # hardcoded
    
    conjunction_min_push_high_input = {k: None for k in conjunction_b4_final.pulse_inputs} 
    
    while any([v is None for v in conjunction_min_push_high_input.values()]):
        button_pushes += 1
        
        frontier = deque(button.trigger())
        
        while frontier:
            pulse = frontier.popleft()
            pulses_sent = pulse.destination.trigger(pulse)
            for pulse_sent in pulses_sent:
                if pulse_sent.destination.name == 'rx':
                    for input_pulse_name, input_pulse_mag in pulse_sent.origin.pulse_inputs.items():
                        if input_pulse_mag == PulseMagnitude.HIGH:
                            conjunction_min_push_high_input[input_pulse_name] = conjunction_min_push_high_input[input_pulse_name] or button_pushes
                    if pulse_sent.magnitude == PulseMagnitude.LOW:
                        return button_pushes
            frontier.extend(pulses_sent)
    return lcm(*conjunction_min_push_high_input.values())

if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
