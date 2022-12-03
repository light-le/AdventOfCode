template = '''
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

@session.submit_result(level=1)
def solve_part1(inp):
    pass

@session.submit_result(level=2)
def solve_part2(inp):
    pass


if __name__ == '__main__':
    inp = session.read_input().split('\\n')[:-1]ß
    
    solve_part1(inp)
    
    solve_part2(inp)
'''

import argparse
import os
parser = argparse.ArgumentParser(description='A script that starts '
                                 'all other scripts based on year input')

parser.add_argument('year', nargs=1, help='Input a year. Ex: 2022', type=int)
args = parser.parse_args()

script_names = {f'day{str(d)}.py' for d in range(1, 26)}

def fabricate_pyscripts(script_names: set=script_names, template:str=template):
    for name in script_names:
        with open(name, mode='w') as pyfile:
            pyfile.write(template)

if __name__ == '__main__':
    year = str(args.year[0])
    if year in os.listdir():
        print(f'Directory {year} already exists, checking if it has all the day scripts')
        os.chdir(year)
        pyscripts = {pyfile for pyfile in os.listdir() if pyfile.endswith('.py')}
        missing_pyscripts = script_names - pyscripts
        if missing_pyscripts:
            print(f"Missing python files {missing_pyscripts} in folder {year}. Making them now")
            fabricate_pyscripts(script_names=missing_pyscripts)
        else:
            print(f"All python scripts {script_names} already existed. Not doing anything.")
    else:
        print(f"Folder {year} not existed yet. Making it now and all of the scripts inside")
        os.mkdir(year)
        os.chdir(year)
        fabricate_pyscripts()