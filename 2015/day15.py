from dataclasses import dataclass
from functools import reduce
from itertools import product
from typing import List
from utils import AdventSession, extract_year_day_from_path

@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int
    
    @classmethod
    def parse_recipe(cls, recipe: str):
        name, cap, capint, dur, durint, fla, flaint, text, textint, cal, calin = recipe.split(' ')
        return cls(name = name[:-1],
                   capacity = int(capint[:-1]),
                   durability = int(durint[:-1]),
                   flavor = int(flaint[:-1]),
                   texture = int(textint[:-1]),
                   calories = int(calin))

def dot_product(vec1: List, vec2: List) -> int:
    return sum(e1*e2 for e1, e2 in zip(vec1, vec2))

def property_product(vec: List) -> int:
    return reduce((lambda a,b: a*b), vec)

def convert_recipes_to_properties(recipes):
    properties = {
        ptype: [vars(recipe).get(ptype) for recipe in recipes]
        for ptype in ['capacity', 'durability', 'texture', 'flavor']
    }
    return properties
    
def solve_part1(properties, recipes):
    possibles = possible_recipes(len(recipes))
    scores = [
        property_product([
            max(dot_product(v1, v2), 0) for v2 in properties.values()
        ]) for v1 in possibles
    ]
    return max(scores)

def possible_recipes(n, length=100):
    products = product(range(length+1), repeat=n)
    possibles = (p for p in products if sum(p) == 100)
    return possibles

def solve_part2(properties, recipes):
    possibles = possible_recipes(len(recipes))
    scores = [
        property_product([
            max(dot_product(v1, v2), 0) for v2 in properties.values()
        ]) for v1 in possibles if dot_product(v1, [rec.calories for rec in recipes]) == 500
    ]
    return max(scores)
if __name__ == '__main__':
    session = AdventSession(**extract_year_day_from_path(__file__))
    
    recipes = [Ingredient.parse_recipe(r) for r in session.read_input().split('\n') if r]
    
    properties = convert_recipes_to_properties(recipes)

    part1_answer = solve_part1(properties, recipes)
    print(part1_answer)
    session.post_answer(part1_answer)
    
    part2_answer = solve_part2(properties, recipes)
    print(part2_answer)
    session.post_answer(part2_answer, level=2)
