from statistics import median, mean

def part1_solution(crabs):
    mid_crab = median(crabs)
    return sum([abs(mid_crab - crab) for crab in crabs])

def incremental_sum(n):
    '''
    sum of all numbers from 1 to n, or (n+1)*(n/2)
    '''
    return (n+1)*(n/2)
    
def part2_solution(crabs):
    mean_crab = int(mean(crabs))
    return sum([incremental_sum(abs(mean_crab-crab)) for crab in crabs])


if __name__ == "__main__":
    with open('2021/day7.txt', 'r') as f:
        crabs = [int(c) for c in f.readline().split(',')]
    print(part1_solution(crabs))
    print(part2_solution(crabs))