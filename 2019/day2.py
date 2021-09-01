
class Codes:
    def __init__(self, codes) -> None:
        self.codes = list(codes)
        self.len = len(self.codes)
    
    def program1(self, pos):
        self.codes[self.codes[pos+3]] = self.codes[self.codes[pos+1]] + self.codes[self.codes[pos+2]]

    def program2(self, pos):
        self.codes[self.codes[pos+3]] = self.codes[self.codes[pos+1]] * self.codes[self.codes[pos+2]]

if __name__ == "__main__":
    with open('2019/day2.txt', 'r') as f:
        line = f.readline().rstrip()
    try_pairs = [(noun, verb) for noun in range(100) for verb in range(100)]
    for noun, verb in try_pairs:
        seq = Codes(map(int, line.split(',')))
        seq.codes[1] = noun
        seq.codes[2] = verb
        i = 0
        while i < seq.len and seq.codes[i] != 99:
            if seq.codes[i] == 1:
                seq.program1(i)
                i+=4
            elif seq.codes[i] == 2:
                seq.program2(i)
                i+=4
            else:
                raise ValueError(f'Stuck in infinite loop at i = {i}, code = {seq.codes[1]}')
        if seq.codes[0] == 19690720:
            print(100*noun+verb)
            break