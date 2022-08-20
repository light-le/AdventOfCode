
from typing import List, Set
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

class Chip(int):
    pass

class Output:
    all_outputs = dict()
    def __init__(self, n: int) -> None:
        self.n = n
        self.__class__.all_outputs[n] = self
        
    def add_chip(self, chip: Chip):
        self.chip = chip
        
    def __repr__(self) -> str:
        return f'Output {self.n} has chip {self.chip}'

class Bot:
    all_bots = dict()
    def __init__(self, n) -> None:
        self.n = n
        self.chips = []
        
        self.__class__.all_bots[n] = self
        self.logic = {
            'low': None,
            'high': None,
        }
    
    def __repr__(self) -> str:
        return f'Bot {self.n} has {self.chips}'
    def add_chip(self, chip: Chip):
        self.chips.append(chip)
        if len(self.chips) == 2:
            low, high = sorted(self.chips)
            

            if self.logic['low']:
                result = self.logic['low'].add_chip(low)
                if result:
                    return result
            self.chips.remove(low)
            if self.logic['high']:
                result = self.logic['high'].add_chip(high)
                if result:
                    return result
            self.chips.remove(high)
            
            if low == Chip(17) and high == Chip(61):
                return self
    def __hash__(self) -> int:
        return hash(self.n)
    
    @classmethod
    def add_bot_if_not_exist(cls, bot_n: int):
        if bot_n in cls.all_bots:
            return cls.all_bots[bot_n]
        bot = Bot(bot_n)
        cls.all_bots[bot_n] = bot
        return bot
    
    
def parse_bot_logic(rule: str):
    bot_, bot_n, give, low, to, bot_output, low_b, *_, bot_output2, high_b = rule.split()
    bot = Bot.add_bot_if_not_exist(int(bot_n))
    
    if bot_output == 'bot':
        low_bot = Bot.add_bot_if_not_exist(int(low_b))
        bot.logic['low'] = low_bot
    elif bot_output == 'output':
        bot.logic['low'] = Output(int(low_b))
    else:
        raise Exception(f'wrong bot output string {bot_output}')
    
    if bot_output2 == 'bot':
        high_bot = Bot.add_bot_if_not_exist(int(high_b))
        bot.logic['high'] = high_bot
    elif bot_output2 == 'output':
        bot.logic['high'] = Output(int(high_b))
    else:
        raise Exception(f'wrong bot2 output string {bot_output2}')
    
    
        
def parse_bot_chip_value(rule: str):
    value, chip_v, goes, to, bot_, bot_n = rule.split()
    bot = Bot.add_bot_if_not_exist(int(bot_n))
    return bot.add_chip(Chip(chip_v))


@session.submit_result(level=1, tests=[({'inp': {
    'value 75 goes to bot 2',
    'bot 2 gives low to bot 1 and high to bot 0',
    'value 17 goes to bot 1',
    'bot 1 gives low to output 1 and high to bot 0',
    'bot 0 gives low to output 2 and high to output 0',
    'value 61 goes to bot 2',
}}, 1)])
def solve_part1(inp: Set[str]):
    bot_logics = {logic for logic in inp if logic.startswith('bot')}
    [parse_bot_logic(logic) for logic in bot_logics]
    
    bot_values = inp-bot_logics
    for bot_value in bot_values:
        answer_bot = parse_bot_chip_value(bot_value)
        if answer_bot is not None:
            return answer_bot.n

    
@session.submit_result(level=2, tests=[({'inp': {
    'value 5 goes to bot 2',
    'bot 2 gives low to bot 1 and high to bot 0',
    'value 3 goes to bot 1',
    'bot 1 gives low to output 1 and high to bot 0',
    'bot 0 gives low to output 2 and high to output 0',
    'value 2 goes to bot 2',
}}, 30)])
def solve_part2(inp: Set[str]):
    bot_logics = {logic for logic in inp if logic.startswith('bot')}
    [parse_bot_logic(logic) for logic in bot_logics]
    [parse_bot_chip_value(value) for value in inp - bot_logics]
    return Output.all_outputs[0].chip * Output.all_outputs[1].chip * Output.all_outputs[2].chip


if __name__ == '__main__':
    inp = {i for i in session.read_input().split('\n') if i}
    
    solve_part1(inp)
    
    solve_part2(inp)
