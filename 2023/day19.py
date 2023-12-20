from __future__ import annotations
from functools import reduce
import json
from typing import Union

from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

MIN_PART_CONDITION = 1
MAX_PART_CONDITION = 4000

def clean_partstr(partstr: str) -> str:
    '''
    Make is json parsable
    '''
    for att in list('xmas'):
        partstr = partstr.replace(att, f'"{att}"')
    return partstr.replace('=', ': ')

def find_ranges_collision(r1: range, r2: range) -> tuple[range, range]:
    '''
    return 2 ranges, 1st is r1 that is in r2, 2nd is r1 that is not in r2
    there will never be a case where r2 is completely within r1, 
    '''
    # print('r1', r1, 'r2', r2)
    if r1.start >= r2.stop or r1.stop <= r2.start: # no collision
        return None, r1
    if r2.start <= r1.start:
        if r1.stop <= r2.stop: # r1 is within r2
            return r1, None
        return range(r1.start, r2.stop), range(r2.stop, r1.stop)
    elif r2.stop >= r1.stop:
        return range(r2.start, r1.stop), range(r1.start, r2.start)
    else:
        raise Exception(f'Invalid ranges r1 {r1} and r2 {r2}')
        

class ConditionCheck:
    def __init__(self, condition: callable, part_att: str=None, true_range: range=None, true_return: str=None) -> None:
        self.condition = condition
        self.part_att = part_att
        self.true_range = true_range
        self.true_return = true_return
        
    @classmethod
    def parse_conditionstr(cls, condstr: str) -> tuple[str, ConditionCheck]:
        if ':' not in condstr:
            return condstr, cls(lambda p: condstr, true_range=range(MIN_PART_CONDITION, MAX_PART_CONDITION+1), true_return=condstr)
        condition_term, true_return = condstr.split(':')
        part_att, condition_sign, *condition_numl = condition_term
        condition_int = int(''.join(condition_numl))
        if condition_sign == '>':
            condifunc = lambda p: true_return if p[part_att] > condition_int else False
            true_range = range(condition_int+1, MAX_PART_CONDITION+1)
        elif condition_sign == '<':
            condifunc = lambda p: true_return if p[part_att] < condition_int else False
            true_range = range(1, condition_int)
        else:
            raise Exception(f'Invalid condition sign {condition_sign}. Original term is {condition_term}')
        
        return true_return, cls(condifunc, part_att, true_range, true_return)
    
    def evaluate(self, part) -> Union[str, bool]:
        return self.condition(part)
    
    def predict_part_ranges(self, part_range: dict) -> tuple[dict, dict]:
        if self.part_att is None:
            if self.true_return == 'R':
                return None, None
            return part_range.copy(), None
        
        range_to_check = part_range[self.part_att]
        true_range, false_range = find_ranges_collision(range_to_check, self.true_range)
        
        true_part_range = part_range.copy()
        false_part_range = part_range.copy()
        
        if true_range is None:
            return None, false_part_range
        elif false_range is None:
            return true_part_range, None

        true_part_range.update({self.part_att: true_range})
        false_part_range.update({self.part_att: false_range})
        
        if self.true_return == 'R':
            return None, false_part_range
        
        return true_part_range, false_part_range
        

class FlowNode:
    def __init__(self, name: str, condition_check: ConditionCheck=None) -> None:
        self.name = name
        self.condition_check = condition_check
        self.branches = list()
        
    def add_branch(self, branch: FlowNode) -> None:
        self.branches.append(branch)
        
    def flow_evaluate(self, part) -> str:
        for next_node in self.branches:
            next_node_evaluation = next_node.condition_check.evaluate(part)
            if next_node_evaluation:
                if next_node_evaluation in ('A', 'R'):
                    return next_node_evaluation
                break
        return next_node.flow_evaluate(part)
    
    def flow_predict(self, part_range: dict) -> dict():
        accepted_parts= 0
        if self.name == 'A':
            print(part_range)
            return reduce(lambda a, b: a*b, [len(r) for r in part_range.values()])
        elif self.name == 'R':
            return 0

        for next_node in self.branches:
            true_part_range, false_part_range = next_node.condition_check.predict_part_ranges(part_range)
            if true_part_range is not None:
                accepteds = next_node.flow_predict(true_part_range)
                accepted_parts += accepteds
                
            if false_part_range is None:
                break

            part_range = false_part_range
        return accepted_parts
    
    def __repr__(self) -> str:
        return f'{self.name} ({"|".join([repr(node) for node in self.branches])})'
        

class FlowTree:
    def __init__(self, head: FlowNode) -> None:
        self.head = head
        
    @classmethod
    def parse_flowstr(cls, flowd: dict, start: str='in') -> FlowTree:
        head_node = FlowNode(start)
        
        frontier = [head_node]
        while frontier:
            node = frontier.pop()
            node_str = flowd[node.name]
        
            for conditionstr in node_str.split(','):
                next_node_name, conditioncheck = ConditionCheck.parse_conditionstr(conditionstr)
                next_node = FlowNode(next_node_name, condition_check=conditioncheck)
                node.add_branch(next_node)
                
                if next_node_name not in ('A', 'R'):
                    frontier.append(next_node)
        return cls(head_node)
    
    def __repr__(self) -> str:
        return repr(self.head)
        
@session.submit_result(level=1, tests=[({'inp': [
    'px{a<2006:qkq,m>2090:A,rfg}',
    'pv{a>1716:R,A}',
    'lnx{m>1548:A,A}',
    'rfg{s<537:gd,x>2440:R,A}',
    'qs{s>3448:A,lnx}',
    'qkq{x<1416:A,crn}',
    'crn{x>2662:A,R}',
    'in{s<1351:px,qqz}',
    'qqz{s>2770:qs,m<1801:hdj,R}',
    'gd{a>3333:R,R}',
    'hdj{m>838:A,pv}',
    '',
    '{x=787,m=2655,a=1222,s=2876}',
    '{x=1679,m=44,a=2067,s=496}',
    '{x=2036,m=264,a=79,s=2244}',
    '{x=2461,m=1339,a=466,s=291}',
    '{x=2127,m=1623,a=2188,s=1013}'
]}, 19114)])
def solve_part1(inp: list[str]):
    parts, flowd = parse_parts_and_flow(inp)

    flow_tree = FlowTree.parse_flowstr(flowd)
    
    return sum([sum(part.values()) for part in parts if flow_tree.head.flow_evaluate(part) == 'A'])

def parse_parts_and_flow(inp):
    flowstr = inp[:inp.index('')]
    partstr = inp[inp.index('')+1:]
    
    parts = [json.loads(clean_partstr(part)) for part in partstr]
    
    flowd = dict()
    for flow in flowstr:
        flow_name, flow_content = flow.split('{')
        flowd[flow_name] = flow_content.replace('}', '')
    return parts,flowd

@session.submit_result(level=2, tests=[({'inp': [
    'px{a<2006:qkq,m>2090:A,rfg}',
    'pv{a>1716:R,A}',
    'lnx{m>1548:A,A}',
    'rfg{s<537:gd,x>2440:R,A}',
    'qs{s>3448:A,lnx}',
    'qkq{x<1416:A,crn}',
    'crn{x>2662:A,R}',
    'in{s<1351:px,qqz}',
    'qqz{s>2770:qs,m<1801:hdj,R}',
    'gd{a>3333:R,R}',
    'hdj{m>838:A,pv}',
    '',
    '{x=787,m=2655,a=1222,s=2876}',
    '{x=1679,m=44,a=2067,s=496}',
    '{x=2036,m=264,a=79,s=2244}',
    '{x=2461,m=1339,a=466,s=291}',
    '{x=2127,m=1623,a=2188,s=1013}'
]}, 167409079868000)])
def solve_part2(inp: list[str]):
    parts, flowd = parse_parts_and_flow(inp)
    
    flow_tree = FlowTree.parse_flowstr(flowd)
    accepted_parts = flow_tree.head.flow_predict(
        part_range={k: range(MIN_PART_CONDITION, MAX_PART_CONDITION+1) for k in list('xmas')})
    
    return accepted_parts
    
if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
