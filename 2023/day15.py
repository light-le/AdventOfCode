from collections import defaultdict
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

def hash_algo(step: str) -> int:
    current_value = 0
    for char in step:
        ascii_value = ord(char)
        current_value += ascii_value
        current_value *= 17
        current_value %= 256
    return current_value
    

@session.submit_result(level=1, tests=[
    ({'inp': 'HASH'}, 52), 
    ({'inp': 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'}, 1320)
])
def solve_part1(inp: str):
    steps = inp.split(',')
    return sum([hash_algo(step) for step in steps])
    
    
@session.submit_result(level=2, tests=[
    ({'inp': 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'}, 145)
])
def solve_part2(inp: str):
    steps = inp.split(',')
    
    boxes = defaultdict(dict)
    
    for step in steps:
        if '=' in step:
            label, sfocal = step.split('=')
            focal = int(sfocal)
            
            boxno = hash_algo(label)
            
            if label in boxes[boxno]:
                old_focal, rank = boxes[boxno][label]
                boxes[boxno][label] = (focal, rank)
            elif not boxes[boxno]:
                boxes[boxno][label] = (focal, 1)
            else:
                max_rank = max([rank for focal, rank in boxes[boxno].values()])
                boxes[boxno][label] = (focal, max_rank+1)
        elif '-' in step:
            label = step.replace('-', '')
            boxno = hash_algo(label)
            if label in boxes[boxno]:
                focal, rank = boxes[boxno].pop(label)
                for label, (lfocal, lrank) in boxes[boxno].items():
                    if lrank > rank:
                        boxes[boxno][label] = (lfocal, lrank-1)
        else:
            raise Exception(f'what is this step {step}?')
    return sum([sum([focal*rank*(boxno+1) for label, (focal, rank) in box.items()]) for boxno, box in boxes.items()])



if __name__ == '__main__':
    inp = session.read_input()[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
