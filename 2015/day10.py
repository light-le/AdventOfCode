from collections import Counter

def apply_look_and_say(line: str, times: int=40):
    for _ in range(times):
        old_line = line
        line = look_and_say(line)
        test_look_and_say_result(old_line, new_line=line)
    return len(line)

def look_and_say(line):
    c = 0
    output = ''
    
    while c < len(line):
        num = line[c]
        count = 0
        while c < len(line) and line[c] == num:
            count += 1
            c+=1
        output += (str(count) + num)
    return output

def test_look_and_say_result(old_line, new_line):
    old_count = Counter(old_line)
    new_count = dict()
    for c in range(0, len(new_line), 2):
        count = int(new_line[c])
        num = new_line[c+1]

        new_count[num] = new_count.get(num, 0) + count

    assert old_count == new_count, f'oldline: {old_line}, newline: {new_line}'

def test_look_and_say():
    in_outs = [('1', '11'), ('11', '21'), ('21', '1211'),
               ('1211', '111221'), ('111221', '312211'),
               ('1113222113', '3113322113')]
    for inp, outp in in_outs:
        assert look_and_say(inp) == outp

if __name__ == '__main__':
    # test_look_and_say()
    from utils import AdventSession, extract_year_day_from_path
    session = AdventSession(**extract_year_day_from_path(__file__))

    line = session.read_input().strip()

    part1_answer = apply_look_and_say(line, times=40)
    print(part1_answer)
    session.post_answer(part1_answer, level=1)

    part2_answer = apply_look_and_say(line, times=50)
    print(part2_answer)
    session.post_answer(part2_answer, level=2)