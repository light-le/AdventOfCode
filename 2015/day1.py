
with open('2015/day1.txt') as f:
    line = f.readline()

floor = 0
for c, char in enumerate(line):
    if char == '(':
        floor += 1
    elif char == ')':
        floor -= 1
    
    if floor == -1:
        print(c+1)
        break