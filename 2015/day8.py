from utils import AdventSession, extract_year_day_from_path

def solve_part1(lines):
    diff = 0
    for line in lines:
        line_diff = 0
        line_diff += 2 # start " and end "
        c = 0
        for s in line:
            print(s, end=' ')
        while c < len(line)-1:
            c += 1
            char = line[c]
            if char == '\\':
                next_char = line[c+1]
                if next_char in ['\\', '"']:
                    line_diff += 1
                    c += 1
                elif next_char == 'x':
                    line_diff += 3
                    c += 3
        print(line_diff)
        diff += line_diff
    return diff

def solve_part2(lines):
    diff = 0
    for line in lines:
        line_diff = 4
        c = 1
        for char in line:
            print(char, end=' ')
        while c < len(line) - 1:
            char = line[c]
            if char in ['\\', '"']:
                line_diff += 1
            c += 1
        
        print(line_diff)
        diff += line_diff
    return diff

if __name__ == '__main__':
    session = AdventSession(**extract_year_day_from_path(__file__))

    lines = [line for line in session.read_input().split('\n') if line]
    
    part1_answer = solve_part1(lines)
    print(part1_answer)
    session.post_answer(part1_answer, level=1)

    part2_answer = solve_part2(lines)
    print(part2_answer)
    session.post_answer(part2_answer, level=2)