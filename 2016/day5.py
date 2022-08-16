from hashlib import md5
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

@session.submit_result(level=1, tests=[({'id': 'abc'}, '18f47a30')])
def solve_part1(id):
    password = ''
    i = 0
    while len(password) < 8:
        combine = id + str(i)
        hashed = md5(combine.encode()).hexdigest()
        if hashed.startswith('00000'):
            password += hashed[5]
        i += 1
    return password

@session.submit_result(level=2, tests=[({'id': 'abc'}, '05ace8e3')])
def solve_part2(id):
    password = ['' for _ in range(8)]
    i = 0
    while len(''.join(password)) < 8:
        combine = id + str(i)
        hashed = md5(combine.encode()).hexdigest()
        if hashed.startswith('00000') and hashed[5].isnumeric():
            ind5 = int(hashed[5])
            if ind5 in range(8) and password[ind5] == '':
                password[ind5] = hashed[6]
        i += 1
    return ''.join(password)

if __name__ == '__main__':
    inp = session.read_input().strip()
    
    solve_part1(inp)
    
    solve_part2(inp)
