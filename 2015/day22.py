from dataclasses import dataclass
from utils import AdventSession, extract_year_day_from_path

stat_shortener = {
    'Hit Points': '_hp',
    'Damage': 'dmg'
}

mana_cost = {
    'magsile' : 53,
    'drain': 73,
    'shield': 113,
    'poison': 173,
    'recharge': 229,
}

@dataclass
class Entity:
    _hp: int = 50
    armor: int = 0
    dmg: int = 0
    
    @property
    def hp(self):
        return self._hp
    
    @hp.setter
    def hp(self, h):
        self._hp = h
        
    def copy(self):
        cls = self.__class__
        return cls(**vars(self))

@dataclass
class Boss(Entity):
    poison_timer: int = 0
    
    def damage(self, player):
        dmg = max(self.dmg - player.armor, 1)
        player.hp -= dmg

@dataclass
class Wizard(Entity):
    _mana: int = 500
    shield_timer: int = 0
    recharge_timer: int = 0
    
    @property
    def mana(self):
        return self._mana
    
    @mana.setter
    def mana(self, m):
        self._mana = m
        
    @property
    def spells(self):
        return {
            'magsile' : self.magic_missile,
            'drain': self.drain,
            'shield': self.shield,
            'poison': self.poison,
            'recharge': self.recharge
        }
        
    def derive_possible_spells(self, boss):
        spells = set(self.spells.keys())
        if self.shield_timer:
            spells.discard('shield')
        if self.recharge_timer:
            spells.discard('recharge')
        if boss.poison_timer:
            spells.discard('poison')
        possible_spell = {spell for spell in spells if mana_cost[spell] <= self.mana}
        return possible_spell

    def cast(self, spell: str, boss):
        self.spells[spell](boss)
    
    def magic_missile(self, boss):
        boss.hp -= 4
        self.mana -= 53
        
    def drain(self, boss):
        self.hp += 2
        boss.hp -= 2
        self.mana -= 73
        
    def shield(self, boss):
        self.armor = 7
        self.mana -= 113
        self.shield_timer = 6
        
    def poison(self, boss):
        self.mana -= 173
        boss.poison_timer = 6
        
    def recharge(self, boss):
        self.mana -= 229
        self.recharge_timer = 5
        

@dataclass(frozen=True)
class StateBoss:
    _hp: int
    dmg: int
    poison_timer: int
    
@dataclass(frozen=True)
class StateWizard:
    _hp: int
    mana: int
    shield_timer: int
    recharge_timer: int

@dataclass(frozen=True)
class State:
    boss: StateBoss
    wizard: StateWizard
    
    
@dataclass(frozen=True)
class FrontierItem:
    state: State
    turn: int = 0
    manacost: int = 0

def solve_part1_and2(player, boss, mode='easy') -> int:
    state = State(
        boss=StateBoss(_hp=boss.hp, dmg=boss.dmg, poison_timer=boss.poison_timer),
        wizard=StateWizard(
            _hp=player.hp,
            mana=player.mana,
            shield_timer=player.shield_timer,
            recharge_timer=player.recharge_timer,
        )
    )
    frontier = {FrontierItem(state)}
    visited_states = {state}
    winning_manas= set()
    
    while frontier:
        frontier_item = frontier.pop()
        turn = frontier_item.turn + 1
        state_boss = frontier_item.state.boss
        state_wizard = frontier_item.state.wizard
        
        boss = Boss(_hp=state_boss._hp, dmg=state_boss.dmg, poison_timer=state_boss.poison_timer)
        wizard = Wizard(
            _hp = state_wizard._hp,
            armor = 7 if state_wizard.shield_timer > 1 else 0,
            _mana = state_wizard.mana,
            shield_timer=state_wizard.shield_timer,
            recharge_timer=state_wizard.recharge_timer,
        )

        if boss.poison_timer:
            boss.hp -= 3
            boss.poison_timer -= 1
            if boss.hp <= 0:
                winning_manas.add(frontier_item.manacost)
                continue
        if wizard.recharge_timer:
            wizard.mana += 101
            wizard.recharge_timer -= 1
        if wizard.shield_timer:
            wizard.shield_timer -= 1

        if turn % 2 == 1:
            if mode == 'hard':
                wizard.hp -= 1
                if wizard.hp <= 0:
                    continue # you lost
            spells = wizard.derive_possible_spells(boss)
            for spell in spells:
                next_boss_state = boss.copy()
                next_wizard_state = wizard.copy()
                
                next_wizard_state.cast(spell, next_boss_state)
                state_mana_cost = frontier_item.manacost + mana_cost[spell]
                
                if next_wizard_state.hp > 0 and next_boss_state.hp > 0 and next_wizard_state.mana >= 0:
                    next_state = State(
                        boss=StateBoss(_hp=next_boss_state.hp,
                                        dmg=next_boss_state.dmg,
                                        poison_timer=next_boss_state.poison_timer),
                        wizard=StateWizard(_hp=next_wizard_state.hp,
                                            mana=next_wizard_state.mana,
                                            shield_timer=next_wizard_state.shield_timer,
                                            recharge_timer=next_wizard_state.recharge_timer)
                    )
                    if next_state not in visited_states:
                        visited_states.add(next_state)
                        frontier.add(FrontierItem(next_state, turn, state_mana_cost))
                elif next_boss_state.hp <= 0:
                    winning_manas.add(state_mana_cost)
                else:
                    pass
                    # print(f"Player lost at wizard state {next_wizard_state} and boss state {next_boss_state}")
        else:
            next_boss_state = boss.copy()
            next_wizard_state = wizard.copy()
            
            next_boss_state.damage(next_wizard_state)
            state_mana_cost = frontier_item.manacost

            if next_wizard_state.hp > 0:
                next_state = State(
                    boss=StateBoss(_hp=next_boss_state.hp,
                                    dmg=next_boss_state.dmg,
                                    poison_timer=next_boss_state.poison_timer),
                    wizard=StateWizard(_hp=next_wizard_state.hp,
                                        mana=next_wizard_state.mana,
                                        shield_timer=next_wizard_state.shield_timer,
                                        recharge_timer=next_wizard_state.recharge_timer)
                )
                if next_state not in visited_states:
                    visited_states.add(next_state)
                    frontier.add(FrontierItem(next_state, turn, state_mana_cost))
            else:
                pass
                # print(f"Player lost at wizard state {next_wizard_state} and boss state {next_boss_state}")
                    
    return min(winning_manas)

if __name__ == '__main__':
    session = AdventSession(**extract_year_day_from_path(__file__))
    
    stats = [inp for inp in session.read_input().split('\n') if inp]
    
    boss_stats = dict()
    for stat in stats:
        prop, pnt = stat.split(': ')
        boss_stats[stat_shortener[prop]] = int(pnt)
    
    boss = Boss(**boss_stats)
    player = Wizard()
    
    part1_answer = solve_part1_and2(player, boss)
    print(part1_answer)
    session.post_answer(part1_answer, level=1)
    
    part2_answer = solve_part1_and2(player, boss, mode='hard')
    print(part2_answer)
    session.post_answer(part2_answer, level=2)