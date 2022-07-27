from requests import session
from utils import AdventSession, extract_year_day_from_path
from string import ascii_lowercase

class Password(list):
    def __init__(self, pw: str) -> None:
        super().__init__(pw)

    def increment(self):
        last_letter = self.pop()
        if last_letter == 'z':
            last_letter = self.pop()
            new_letters = ['a']
            while last_letter == 'z':
                new_letters.append('a')
                last_letter = self.pop()
            new_letters = [ascii_lowercase[ascii_lowercase.index(last_letter)+1]] + new_letters
            self.extend(new_letters)
        else:
            self.append(ascii_lowercase[ascii_lowercase.index(last_letter)+1])

    def check_that_password_has_straight(self) -> bool:
        strindex = [ascii_lowercase.index(c) for c in self]
        strindiff = [upper - lower for upper, lower in zip(strindex[1:], strindex[:-1])]
        for d, diff in enumerate(strindiff):
            if diff == 1:
                if d < (len(strindiff)-1) and strindiff[d+1] == 1:
                    return True
        return False

    def check_that_password_has_no_iol(self) -> bool:
        return not any(forbidden in self for forbidden in {'i', 'o', 'l'})

    def check_that_password_has_2_non_overlaping_pairs(self) -> bool:
        count = 0
        for letter in ascii_lowercase:
            if letter*2 in str(self):
                count+=1
                if count >= 2:
                    return True
        return False

    def password_check(self) -> bool:
        return all([self.check_that_password_has_straight(),
                    self.check_that_password_has_no_iol(),
                    self.check_that_password_has_2_non_overlaping_pairs()
                ])

    def __str__(self) -> str:
        return ''.join(self)

def update_password(p):
    while not p.password_check():
        p.increment()
    return str(p)

def update_password(p):
    while not p.password_check():
        p.increment()
    return str(p)

if __name__ == '__main__':
    session = AdventSession(**extract_year_day_from_path(__file__))

    password = Password(session.read_input().strip())

    part1_answer = update_password(password)
    print(part1_answer)
    session.post_answer(part1_answer, level=1)

    next_password = Password(part1_answer)
    next_password.increment()
    part2_answer = update_password(next_password)
    print(part2_answer)
    session.post_answer(part2_answer, level=2)