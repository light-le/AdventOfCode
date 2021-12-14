from collections import Counter

def part1_solution(temps, rules):
    all_pairs = []
    for step in range(10):
        pairs = [temps[i]+ temps[i+1] for i in range(len(temps)-1)]
        all_pairs.extend(pairs)
        poly_add = [rules[p] for p in pairs]
        new_temps = [pairs[i][0] + poly_add[i] for i in range(len(pairs))]
        temps = ''.join(new_temps) + temps[-1]
        count_chars = Counter(temps).most_common()
    return count_chars[0][1] - count_chars[-1][1]

def part2_solution(temps, rules):
    last_element = temps[-1]
    temp_pairs = [temps[i]+ temps[i+1] for i in range(len(temps)-1)]
    pair_count = dict(Counter(temp_pairs))
    for step in range(40):
        children = dict()
        for parent, count in pair_count.items():
            for child in rules[parent]:
                if child in children:
                    children[child] += count
                else:
                    children[child] = count
        pair_count = children.copy()
    element_count = dict()
    for pair, count in pair_count.items():
        element = pair[0]
        if element in element_count:
            element_count[element] += count
        else:
            element_count[element] = count
    element_count[last_element] += 1
    count_list = list(element_count.values())
    return max(count_list) - min(count_list)


if __name__ == "__main__":
    with open('2021/day14.txt', 'r') as f:
        lines = f.read().rsplit(sep='\n')
    template, linebreak, *insert_rules = lines
    rule_split = [rule.split(' -> ') for rule in insert_rules]
    rules = {k: v for k, v in rule_split}
    prules = {k: [k[0] + v, v+k[1]] for k, v in rules.items()}
    print(part1_solution(template, rules))
    print(part2_solution(template, prules))
