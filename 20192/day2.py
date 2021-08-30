from typing import List


with open('2019/day2.txt', 'r') as f:
    line = f.readline().rstrip()

class Codes:
    def __init__(self, codes) -> None:
        self.codes = list(codes)
        self.len = len(self.codes)
    
    def program1(self, pos):
        self.codes[self.codes[pos+3]] = self.codes[self.codes[pos+1]] + self.codes[self.codes[pos+2]]

    def program2(self, pos):
        self.codes[self.codes[pos+3]] = self.codes[self.codes[pos+1]] * self.codes[self.codes[pos+2]]

seq = Codes(map(int, line.split(',')))

i = 0
seq.codes[1] = 12
seq.codes[2] = 2
while i < seq.len and seq.codes[i] != 99:
    if seq.codes[i] == 1:
        seq.program1(i)
        i+=4
    elif seq.codes[i] == 2:
        seq.program2(i)
        i+=4
print(seq.codes[0])