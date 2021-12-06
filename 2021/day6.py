from collections import Counter

def part1_solution(fishes, days=80):
    fhs = fishes.copy()
    for day in range(days):
        fhs.extend([9]*fhs.count(0))
        for f, fish in enumerate(fhs):
            if fish > 0:
                fhs[f]-=1
            else:
                fhs[f]=6
    return len(fhs)


def part2_solution(fishes, days):
    fish_count = dict(Counter(fishes))
    for day in range(days):
        fish_at_0 = fish_count.get(0, 0)

        fish_count = {f-1:c for f, c in fish_count.items()}
        
        fish_at_6 = fish_count.get(6, 0)
        fish_count[6] = fish_at_6 + fish_at_0
        if fish_at_0 > 0:
            del fish_count[-1]
        fish_count[8] = fish_at_0
    return sum(list(fish_count.values()))


if __name__ == "__main__":
    with open('2021/day6.txt', 'r') as f:
        fishes = [int(fish) for fish in f.readline().split(',')]

    print(part1_solution(fishes))
    print(part2_solution(fishes, 256))