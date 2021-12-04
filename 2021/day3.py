
def part1_solution(bits):
    bit_transposed = [[line[i] for line in bits] for i in range(len(bits[0]))]

    grate = ''
    erate = ''
    for bit in bit_transposed:
        if bit.count('1') > bit.count('0'):
            grate += '1'
            erate += '0'
        else:
            grate += '0'
            erate += '1'
    return int(grate, 2)*int(erate, 2)

def part2_solution(bits):
    # bit_transposed = [[line[i] for line in bits] for i in range(len(bits[0]))]

    O2rate = bits.copy()
    CO2rate = bits.copy()

    for i in range(len(bits[0])):
        if len(O2rate) > 1:
            O2_ibits = [r[i] for r in O2rate]
            if O2_ibits.count('1') >= len(O2_ibits)/2:
                O2rate = [r for r in O2rate if r[i] == '1']
            else:
                O2rate = [r for r in O2rate if r[i] == '0']

        if len(CO2rate) > 1:
            CO2_ibits = [r[i] for r in CO2rate]
            if CO2_ibits.count('1') >= len(CO2_ibits)/2:
                CO2rate = [r for r in CO2rate if r[i] == '0']
            else:
                CO2rate = [r for r in CO2rate if r[i] == '1']

    if len(O2rate) > 1 or len(CO2rate) > 1:
        raise ValueError('must have len of 1', O2rate, CO2rate)
    return int(''.join(O2rate[0]), 2) * int(''.join(CO2rate[0]), 2)



if __name__ == '__main__':
    with open('2021/day3.txt', 'r') as f:
        lines = f.read().rsplit()

    bits = [[c for c in line] for line in lines]
    print(part1_solution(bits))
    print(part2_solution(bits))