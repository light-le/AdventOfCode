from string import ascii_lowercase
from utils import extract_year_day_from_path, AdventSession

class String:
    def __init__(self, string: str) -> None:
        self.string = string
    
    def contains_at_least_3_vowels(self) -> bool:
        vowels = set('aeiou')
        return len([common_vowel for common_vowel in self.string if common_vowel in vowels]) >=3

    def contains_at_least_1_double_letter(self) -> bool:
        double_letters = [letter*2 for letter in ascii_lowercase]
        return any(double_letter in self.string for double_letter in double_letters)

    def does_not_contains_certain_strings(self) -> bool:
        prohibited_strings = ['ab', 'cd', 'pq', 'xy']
        return not any(prohibited in self.string for prohibited in prohibited_strings)

    def evaluate_part1(self) -> str:
        if all([self.contains_at_least_3_vowels(),
               self.contains_at_least_1_double_letter(),
               self.does_not_contains_certain_strings()]):
            return 'nice string'
        else:
            return 'bad string'

    def contains_pair_of_2_letters_twice(self) -> bool:
        for c in range(len(self.string)-3):
            if self.string[c:c+2] in self.string[c+2:]:
                return True
        return False

    def contains_1_letter_repeat_with_1_letter_between(self) -> bool:
        for c in range(len(self.string)-2):
            if self.string[c] == self.string[c+2]:
                return True
        return False

    def evaluate_part2(self) -> str:
        if all([self.contains_pair_of_2_letters_twice(),
                self.contains_1_letter_repeat_with_1_letter_between()]):
            return 'nice string'
        else:
            return 'bad string'


def solve_part1(strings):
    return len([string for string in strings if string.evaluate_part1() == 'nice string'])

def solve_part2(strings):
    return len([string for string in strings if string.evaluate_part2() == 'nice string'])

if __name__ == '__main__':
    session = AdventSession(**extract_year_day_from_path(__file__))
    input = session.read_input()
    
    strings = [String(line) for line in input.split()]

    # part1_answer = solve_part1(strings)
    # ans1_result = session.post_answer(part1_answer, level=1)
    # print('Part1:', part1_answer, ans1_result)

    part2_answer = solve_part2(strings)
    ans2_result = session.post_answer(part2_answer, level=2)
    print('Part2:', part2_answer, ans2_result)