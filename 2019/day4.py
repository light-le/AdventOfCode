from collections import Counter

def has_double(n):
    nstr = str(n)
    return len(set(nstr)) < len(nstr)

def digit_increase(n):
    nstr = str(n)
    return all([nstr[i+1] >= nstr[i] for i in range(len(nstr)-1)])

def solve_part1():
    passcount = 0
    for num in range(377777, 900000):  # numbers has been derived from inputs
        if has_double(num) and digit_increase(num):
            passcount+=1
    print(f'Part1: {passcount}')

def has_double_only(n):
    ncount = Counter(str(n))
    return 2 in ncount.values()

def solve_part2():
    passcount = 0
    for num in range(377777, 900000):
        if has_double_only(num) and digit_increase(num):
            passcount+=1
    print(f'Part2: {passcount}')


solve_part1()
solve_part2()