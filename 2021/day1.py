
def part1_solution(lint):
    increasing_items = [i for i in range(len(lint)-1) if lint[i+1] > lint[i]]
    print(len(increasing_items))

def part2_solution(lint):
    sliding_sums = [(lint[i] + lint[i+1] + lint[i+2]) for i in range(len(lint)-2)]
    part1_solution(sliding_sums)

if __name__ == '__main__':
    with open('2021/day1.txt', 'r') as inputf:
        lines = inputf.read().rsplit()
        lint = [int(line) for line in lines]
    part1_solution(lint)
    part2_solution(lint)
