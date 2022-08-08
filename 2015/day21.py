from dataclasses import dataclass, field
from typing import List
from itertools import combinations, product
from utils import AdventSession, extract_year_day_from_path

stat_shortener = {
    'Hit Points': 'maxhp',
    'Damage': 'dam',
    'Armor': 'arm'
}

@dataclass
class Entity:
    maxhp:int = field(default=100)
    dam:int = field(default=0)
    arm:int = field(default=0)

    def __post_init__(self):
        self.reset_hp()
        
    def reset_hp(self):
        self.hp = self.maxhp
    
    def calculate_damage(self, dam: int) -> int:
        return max(dam - self.arm, 1)

    def fight(self, other):
        while True:
            other.hp -= other.calculate_damage(self.dam)
            if other.hp <= 0:
                return self
            self.hp -= self.calculate_damage(other.dam)
            if self.hp <= 0:
                return other


@dataclass
class Equipment:
    cost: int
    dam:int = field(default=0)
    arm:int = field(default=0)
    
    def __len__(self):
        return 1
    
class Weapon(Equipment):
    pass

class Armor(Equipment):
    pass

class Ring(Equipment):
    pass

class Boss(Entity):
    pass

class Player(Entity):
    def reset_stat(self):
        self.reset_hp()
        self.dam = 0
        self.arm = 0
        
    def equip_items(self, *items: List[Equipment]):
        for item in items:
            if item is None:
                continue
            if len(item) == 2:
                for each_ring in item:
                    self.dam += each_ring.dam
                    self.arm += each_ring.arm
            else:
                self.dam += item.dam
                self.arm += item.arm

weapons = [Weapon(cost, dam) for cost, dam in [
    (8, 4),
    (10, 5),
    (25, 6),
    (40, 7),
    (75, 8)
]]

armors = [Armor(cost, arm) for cost, arm in [
    (13, 1),
    (31, 2),
    (53, 3),
    (75, 4),
    (102, 5)
]]

rings = [Ring(cost, dam) for cost, dam in [
    (25, 1),
    (50, 2),
    (100, 3)
]] + [Ring(cost, arm) for cost, arm in [
    (20, 1),
    (40, 2),
    (80, 3)
]]

weapon_options = weapons
armor_options = armors + [None]
ring_options = [None] + rings + list(combinations(rings, 2))

war_options = product(weapon_options, armor_options, ring_options)

def calculate_cost(*items: List[Equipment]) -> int:
    cost = 0
    for item in items:
        if item is None:
            continue
        if len(item) == 2:
            cost += sum([ring.cost for ring in item])
        else:
            cost += item.cost
    return cost

def solve_part1_and_part2(p, b) -> int:
    
    minimum_cost = float('Inf')
    maximum_cost = 0
    
    fight_results = dict() # for caching
    
    for weapon, armor, ring in war_options:
        p.reset_stat()
        b.reset_hp()

        p.equip_items(weapon, armor, ring)
        
        pstats = (p.dam, p.arm)
        if pstats not in fight_results:
            winner = p.fight(b)
            fight_results[pstats] = winner
        else:
            winner = fight_results.get(pstats)
            
        fight_cost = calculate_cost(weapon, armor, ring)
        if winner == p:
            minimum_cost = min(minimum_cost, fight_cost)
        else:
            maximum_cost = max(maximum_cost, fight_cost)

    return minimum_cost, maximum_cost


if __name__ == '__main__':
    session = AdventSession(**extract_year_day_from_path(__file__))
    
    stats = session.read_input().split('\n')
    boss_stats = dict()
    
    for stat in stats:
        if not stat:
            continue
        name, score = stat.split(': ')
        boss_stats[stat_shortener[name]] = int(score)
        
    boss = Boss(**boss_stats)
    player = Player()
    
    part1_answer, part2_answer = solve_part1_and_part2(player, boss)
    print(part1_answer)
    session.post_answer(part1_answer, level=1)
    
    print(part2_answer)
    session.post_answer(part2_answer, level=2)
    
    