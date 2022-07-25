from dataclasses import dataclass
from collections import deque
from copy import deepcopy
from utils import extract_year_day_from_path, AdventSession


@dataclass
class WireSignal:
    source1: str
    command: str
    destination: str
    source2: str = None

    destinations = dict()
    max_signal = 65535

    def __post_init__(self) -> None:
        cls = self.__class__
        cls.destinations[self.destination] = self

    @classmethod
    def parse_signal(cls, signal: str):
        source, destination = signal.split(' -> ')
        if ' ' not in source:
            return cls(source1=source, command='ASSIGN', destination=destination)
        *source2, command, source1 = source.split(' ')
        if source2:
            [source2] = source2
            return cls(source1=source1, command=command, destination=destination, source2=source2)
        return cls(source1=source1, command=command, destination=destination)

    def evaluate(self) -> int:
        if self.command == 'ASSIGN':
            return int(self.source1)
        elif self.command == 'AND':
            return int(self.source1) & int(self.source2)
        elif self.command == 'OR':
            return int(self.source1) | int(self.source2)
        elif self.command == 'LSHIFT':
            return int(self.source2) << int(self.source1)
        elif self.command == 'RSHIFT':
            return int(self.source2) >> int(self.source1)
        elif self.command == 'NOT':
            return self.max_signal - int(self.source1)
        else:
            raise Exception(f'Invalid command {self.command}')

    @classmethod
    def stuck_part1(cls):
        '''TOP DOWN APPROACH - DID NOT WORK!!!'''
        frontier = deque([cls.destinations['a']])
        path_to_a = []
        known_paths = set()
        while frontier:
            # FIFO
            signal = frontier.popleft()
            print(signal.destination)
            path_to_a.append(signal)
            known_paths.add(signal.destination)

            if not signal.source1.isnumeric() and signal.source1 not in known_paths:
                frontier.append(cls.destinations[signal.source1])
            if signal.source2 and not signal.source2.isnumeric() and signal.source2 not in known_paths:
                frontier.append(cls.destinations[signal.source2])

        signal_values = dict()
        print(path_to_a)
        while path_to_a:
            print(len(path_to_a))
            signal = path_to_a.pop()
            if not signal.source1.isnumeric():
                signal.source1 = str(signal_values[signal.source1])
            if signal.source2 and not signal.source2.isnumeric():
                signal.source2 = str(signal_values[signal.source2])

            signal_values[signal.destination] = signal.evaluate()

        return signal_values['a']

    @classmethod
    def solve_part(cls, overide_b=None):
        '''Bottom up approach'''
        all_destinations = deepcopy(cls.destinations)
        if overide_b:
            all_destinations['b'] = WireSignal(str(overide_b), 'ASSIGN', 'b')

        frontier = deque([signal for _, signal in all_destinations.items()
                          if signal.source1.isnumeric() and signal.command=='ASSIGN'])
        signal_values = dict()

        while signal_values.get('a') is None:
            signal = frontier.popleft()

            sigval = signal.evaluate()
            signal_values[signal.destination] = sigval

            for _, next_signal in all_destinations.items():
                if next_signal.source1 == signal.destination:
                    next_signal.source1 = str(sigval)
                    if next_signal.source2 is None or next_signal.source2.isnumeric():
                        frontier.append(next_signal)
                elif next_signal.source2 and next_signal.source2 == signal.destination:
                    next_signal.source2 = str(sigval)
                    if next_signal.source1.isnumeric():
                        frontier.append(next_signal)
        return signal_values.get('a')


if __name__ == '__main__':
    session = AdventSession(**extract_year_day_from_path(__file__))
    input = session.read_input()

    signals = [WireSignal.parse_signal(line)
               for line in input.split('\n') if line]

    part1_answer = WireSignal.solve_part()
    print(part1_answer)
    part1_result = session.post_answer(part1_answer, level=1)

    part2_answer = WireSignal.solve_part(overide_b=part1_answer)
    print(part2_answer)
    part2_result = session.post_answer(part2_answer, level=2)

