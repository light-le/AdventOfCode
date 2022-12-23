from typing import Dict, List, Set
from enum import Enum
from functools import reduce
from math import ceil
from collections import namedtuple, Counter, deque
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

State = namedtuple('State', ['minute', 'robot_counter', 'material_counter'])

StateSet = namedtuple("StateSet", ['minute', 'robotub', 'mattub'])

def convert_stateset_to_state(stateset: StateSet) -> State:
    return State(stateset.minute, Counter({r: c for r, c in stateset.robotub}), Counter({m: c for m, c in stateset.mattub}))

def convert_state_to_stateset(state: State) -> StateSet:
    return StateSet(state.minute,
                    tuple(sorted(state.robot_counter.items(),
                                 key=(lambda c: c[0].type.name))),
                    tuple(sorted(state.material_counter.items(),
                                 key=(lambda c: c[0].name)))
                    )

class Material(Enum):
    ORE = 1
    CLAY = 2
    OBSIDIAN = 3
    GEODE = 4
    
    @staticmethod
    def calculate_points(materials: Counter) -> int:
        return sum(mat.value*mat_count for mat, mat_count in materials.items())
    
class Robot:
    def __init__(self, type: Material, cost: Dict) -> None:
        self.type = type
        self.cost = cost
    def __repr__(self) -> str:
        return f'{self.type.name} bot'
    
    def can_be_built_with(self, available_bot_types: List[Material]) -> bool:
        '''
        derive if this bot can be built (with time) with other bot types
        '''
        return set(available_bot_types) >= set(self.cost)
    
        
class Blueprint:
    def __init__(self, id: int, bot_construct: Dict, max_minute: int) -> None:
        self.id = id
        self.bot_construct = bot_construct
        self.max_minute = max_minute
    
    def get_max_cost_of(self, material: Material) -> int:
        return max(robot.cost.get(material, 0) for robot in self.bot_construct.values())
        
    def __repr__(self) -> str:
        return f'ID {self.id}. Bot {self.bot_construct}'
    
    def derive_next_bot_build_states(self, state: State) -> List[State]:
        '''
        From 1 state bots, findout what bot, and when they can be build, one bot at at ime
        Also filter out bots that have reaches the number needed, which is the max materials needed to build another bot
        except for geode bot because we never get enough of them
        '''
        enough_bots = {bot for bot, bot_count in state.robot_counter.items() if bot.type != Material.GEODE and bot_count >= self.get_max_cost_of(bot.type)}
        bots_can_be_built = self.derive_next_bot_builds(state.robot_counter)
        bots_should_be_built = bots_can_be_built - (bots_can_be_built & enough_bots)
        return [self.derive_minute_materials_to_build(bot, state) for bot in bots_should_be_built]
    
    def derive_next_bot_builds(self, bot_counter: Counter) -> Set[Robot]:
        '''
        derive what bots can be built from current bots, based on materials needed
        '''
        return {bot for bot in self.bot_construct.values() if bot.can_be_built_with([bot.type for bot in bot_counter])}
    
    def derive_minute_materials_to_build(self, bot: Robot, state: State) -> State:
        '''
        given the next possible bot builds, determine the minute it would finish for that
        bot to be active, and the material at that state
        If already passes that MAX_MINUTE, return the state at MAX_MINUTE
        '''
        current_minute, state_bot, current_material = state
        material_needed = Counter(bot.cost) - current_material
        state_bot_material_counter = {bot.type: bot_count for bot, bot_count in state_bot.items()}
        
        minutes_to_accumulate_each_materials = {
            mat: ceil(needed_mat_count / state_bot_material_counter[mat])
            for mat, needed_mat_count in material_needed.items()
        }
        # print(bot, current_material)
        # print(minutes_to_accumulate_each_materials, material_needed, state_bot_material_counter)
        
        minutes_to_build = max(minutes_to_accumulate_each_materials.values(), default=0) + 1 # including build time
        
        next_state_minute = current_minute + minutes_to_build
        
        if next_state_minute >= self.max_minute:
            return self.derive_final_state(state)
        else:
            return self.derive_next_state(next_state_minute, bot, state)
        
    def derive_final_state(self, state: State) -> State:
        '''
        Final state is the state at MAX_MINUTE where there's not enough time to build any bot
        '''
        delta_minute = self.max_minute - state.minute
        final_materials = state.material_counter + Counter({
            bot.type: bot_count*delta_minute for bot, bot_count in state.robot_counter.items()
        })
        return State(self.max_minute, state.robot_counter, final_materials)
        
        
    def derive_next_state(self, next_minute: int, bot: Robot, state: State) -> State:
        '''
        Given the next minute, the current state, and the robot to be built,
        determine the materials at that state
        '''
        delta_minute = next_minute - state.minute
        # print(state, delta_minute)
        materials_produced = Counter({
            bot.type: bot_count*delta_minute for bot, bot_count in state.robot_counter.items()
        })
        
        next_state_materials = state.material_counter + materials_produced - Counter(bot.cost)
        return State(next_minute, state.robot_counter + Counter([bot]), next_state_materials)
        
    def solve_for_max_geode(self) -> int:
        frontier = {StateSet(minute=0,
                             robotub=((self.bot_construct[Material.ORE], 1),),
                             mattub=())}
        # deque([State(minute=0,
        #                         robot_counter=Counter([self.bot_construct[Material.ORE]]),
        #                         material_counter=Counter())])
        max_geode = 0
        # final_states = list()
        while frontier:
            state = convert_stateset_to_state(frontier.pop())
            
            for next_new_state in self.derive_next_bot_build_states(state):
                if next_new_state.minute == self.max_minute:
                    max_geode = max(max_geode, next_new_state.material_counter[Material.GEODE])
                    # final_states.append(next_new_state)
                    str_len = str(len(frontier))
                    if str_len.endswith('00000'):
                        print(f'ID {self.id} currently maxgeode {max_geode}. There are {str_len[:-6]} {str_len[-6:-3]} {str_len[-3:]} states in frontier')
                else:
                    frontier.add(convert_state_to_stateset(next_new_state))

        print(f'ID {self.id} final maxgeode {max_geode}')
        return max_geode

def parse_line(line: str, max_minute: int) -> Blueprint:
    bp_id, bot_construct = line.split(': ')
    bp, id = bp_id.split(' ')
    
    ore_bot, clay_bot, obs_bot, geo_bot = bot_construct.split('. ')
    
    *_, ores, ore = ore_bot.split(' ')
    orebot = Robot(Material.ORE, {Material.ORE: int(ores)})
    
    *_, ores, ore = clay_bot.split(' ')
    claybot = Robot(Material.CLAY, {Material.ORE: int(ores)})
    
    *_, ores, ore, and_, clays, clay = obs_bot.split(' ')
    obsbot = Robot(Material.OBSIDIAN, {Material.ORE: int(ores), Material.CLAY: int(clays)})

    *_, ores, ore, and_, obs, ob = geo_bot.split(' ')
    geobot = Robot(Material.GEODE, {Material.ORE: int(ores), Material.OBSIDIAN: int(obs)})
    
    return Blueprint(int(id), bot_construct = {
        Material.ORE: orebot,
        Material.CLAY: claybot,
        Material.OBSIDIAN: obsbot,
        Material.GEODE: geobot
    }, max_minute=max_minute)


@session.submit_result(level=1, tests=[({'inp': [
    'Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.',
    'Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.'
]}, 33)])
def solve_part1(inp):
    blueprints = [parse_line(line, 24) for line in inp]
    return sum(blueprint.id*blueprint.solve_for_max_geode() for blueprint in blueprints)
                
@session.submit_result(level=2, tests=[({'inp': [
    'Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.',
    'Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.'
]}, 62*56)])
def solve_part2(inp):
    blueprints = [parse_line(line, 32) for line in inp]
    return reduce((lambda a, b: a*b), [blueprint.solve_for_max_geode() for blueprint in blueprints[:3]])

if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
