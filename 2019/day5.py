import day2

class Codes2(day2.Codes):
    def __init__(self, codes, inp) -> None:
        super().__init__(codes)
        self.inp = inp

    def program3(self, i):
        self.codes[self.codes[i+1]] = self.inp
    def program4(self, i):
        if self.codes[self.codes[i+1]] != 0:
            raise ValueError(f'test unsuccessful, i: {i}, pos {self.codes[i+1]}, output value {self.codes[self.codes[i+1]]} should be 0')
    def program5(self, i):
        if self.codes[self.codes[i+1]] != 0:
            return self.codes[i+2]
        return i+3
    def program6(self, i):
        if self.codes[self.codes[i+1]] == 0:
            return self.codes[i+2]
        return i+3
    def program7(self, i):
        if self.codes[self.codes[i+1]] < self.codes[self.codes[i+2]]:
            self.codes[self.codes[i+3]] = 1
        else:
            self.codes[self.codes[i+3]] = 0
    def program8(self, i):
        if self.codes[self.codes[i+1]] == self.codes[self.codes[i+2]]:
            self.codes[self.codes[i+3]] = 1
        else:
            self.codes[self.codes[i+3]] = 0
    def pro_param(self, i):
        code = str(self.codes[i])
        opcode = int(code[-1])
        
        param_modes = code[:-2][::-1]
        param_modes += '0'*(3-len(param_modes))

        assert param_modes[-1] == '0', f'Error: last digit of param modes must be 0 to write position. code {code} at i {i}'
        assert all([pm in ['1', '0'] for pm in param_modes]), f'Error: param modes can only be 1 or 0. code {code} at i {i}'

        if opcode in [1, 2]:
            param1, param2 = [self.codes[i+1+c] if param_modes[c] == '1' else self.codes[self.codes[i+1+c]] for c in range(0, 2)]
            pos = self.codes[i+3]
            if opcode == 1:
                self.codes[pos] = param1+param2
            else:
                self.codes[pos] = param1*param2
            return i+4
        elif opcode == 3:
            if param_modes[0] == 0:
                self.codes[self.codes[i+1]] = self.inp
                return i+2
            else:
                raise ValueError(f'No idea how to handle this code {code} at i {i}')
        elif opcode == 4:
            if param_modes[0] == 0:
                test = self.codes[self.codes[i+1]]
            else:
                test = self.codes[i+1]
            if test != 0:
                raise ValueError(f'test unsuccessful, i: {i}, pos {self.codes[i+1]}, output value {self.codes[self.codes[i+1]]} should be 0')
            return i+2
        elif opcode in [5, 6]:
            param1, param2 = [self.codes[i+1+c] if param_modes[c] == '1' else self.codes[self.codes[i+1+c]] for c in [0, 1]]
            if opcode == 5 and param1 != 0:
                return param2
            elif opcode == 6 and param1 == 0:
                return param2
            else:
                return i+3
        elif opcode in [7, 8]:
            param1, param2 = [self.codes[i+1+c] if param_modes[c] == '1' else self.codes[self.codes[i+1+c]] for c in [0, 1]]
            if opcode == 7 and param1 < param2:
                self.codes[self.codes[i+3]] = 1
            elif opcode == 8 and param1 == param2:
                self.codes[self.codes[i+3]] = 1
            else:
                self.codes[self.codes[i+3]] = 0
            return i+4
        else:
            raise ValueError(f'Opcode can only be 1 2 3 4 5 6 7 8')


def solve_part(line, inp):

    program = Codes2(map(int, line.split(',')), inp)

    i = 0
    while i < program.len:
        code = program.codes[i]
        print(program.codes[i:i+4])
        if code == 1:
            program.program1(i)
            i+=4
        elif code == 2:
            program.program2(i)
            i+=4
        elif code == 3:
            program.program3(i)
            i+=2
        elif code == 4:
            program.program4(i)
            i+=2
        elif code == 5:
            i = program.program5(i)
        elif code == 6:
            i = program.program6(i)
        elif code == 7:
            program.program7(i)
            i+=4
        elif code == 8:
            program.program8(i)
            i+=4
        elif code > 99:
            print(program.codes[i:i+4])
            i=program.pro_param(i)
        elif code == 99:
            break


if __name__ == '__main__':
    with open('day5.txt', 'r') as f:
        line = f.readline().strip()
    solve_part(line, 1)  # use the output value ... as answer in the ValueError message
    solve_part(line, 5) # # use the output value ... as answer in the ValueError message