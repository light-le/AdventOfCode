from functools import reduce
from operator import sub
tests = {
    '8A004A801A8002F478': 16,
    '620080001611562C8802118E34': 12,
    'C0015000016115A2E0802F182340': 23,
    'A0016C880162017C3686B18A3D4780': 31,
}

typeid_ops = {
    0: 'sum([',
    1: 'product([',
    2: 'min([',
    3: 'max([',
    5: 'greater([',
    6: 'less([',
    7: 'equal(['
}
def hex_to_bin(hex):
    conversion = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111',
    }
    return ''.join([conversion[h] for h in hex])

def product(li):
    return reduce((lambda a,b: a*b), li)

def greater(li):
    a, b = li
    return 1 if a > b else 0
def less(li):
    a, b = li
    return 1 if a < b else 0
def equal(li):
    a, b = li
    return 1 if a == b else 0

def recursive_read(b, versionsum=0):
    if not b or all([c=='0' for c in b]):
        return versionsum
    version = int(b[:3], 2)
    # print(b, version)
    versionsum+=version
    typeid = int(b[3:6], 2)
    if typeid == 4:
        total_rep = 0
        start_bit = 6
        while b[start_bit] == '1':
            five_bits = b[start_bit:start_bit+5]
            total_rep += int(five_bits[1:], 2)
            start_bit += 5
        five_bits = b[start_bit:start_bit+5]
        total_rep += int(five_bits[1:], 2)
        start_bit += 5
        versionsum = recursive_read(b[start_bit:], versionsum)
    else:
        length_type_id = b[6]
        if length_type_id == '0':
            total_bits_length = int(b[7:22], 2)
            versionsum = recursive_read(b[22:22+total_bits_length], versionsum)
            versionsum = recursive_read(b[22+total_bits_length:], versionsum)
        else:
            subpacket_number = int(b[7:18], 2)
            versionsum = recursive_read(b[18:], versionsum)
    return versionsum


def part1_solution(b):
    version_sum = recursive_read(b, versionsum=0)
    return version_sum

'''
011 000 1 00000000010 000 000 0 000000000010110 000 100 01010 101 100 01011    001 000 1 00000000010 000 100 01100 011 100 01101 00
3                                                             5              1                                  3
110 000 1 00000000010 110 100 00001 010 100 00010
100 010 0 000000000100001 101 100 00111 110 100 01000 000100 01001 0

100 111 0 000000001010000 010 000 1 00000000010 010 100 00001 100 100 00011 110 001 1 00000000010 000 100 00010 010 100 00010 00
equal([sum([1,3]),product([2, 2])])

equal(2,sum(2,1,3,product(2,2,2

000 000 0 001010100000100 001 100 10011 00110 101 001 1 00000000010 110 110 1 00000000010 110 100 00111 000 100 00111 000 100 11100 01111 011 100 10111 10100 11110 11001 01001 011 001 1 00000000010 101 100 11111 11100 00001 011 110 1 00000000010 101 100 11101 00101 011 100 10110 11011 10111 11001 01101 010 100 10111 11010 10110 11110 11010 11011 01010 010 001 1 00000000011 111 100 11001 01010 101 100 11101 01010 011 100 11100 00011 100 001 0 000000000100000  000 100 11101 00101 010 100 11100 01001  101 100 00011 001 001 1 00000000100 110 100 11000 00010 011 100 10101 00101 111 100 11000 00110 101 100 10101 00100 011 010 0 000000000010110  110 100 01110 010 100 01100  001 010 1 00000000001 010 100 10001 11111 00000 011 011 0 000000001001001  011 100 11110 11110 11011 10100 11111 11000 00000 011 100 11011 11110 00100 011 100 00110  101 001 1 00000000010 010 100 10010 01100 000 101 1 00000000010 111 100 11100 11111 11100 1101
sum                                         54 , prod(                  less(                       7,7)                             207),                              478873, prod2(                                   4033                  ,less2(                213,                              440221)),                                       128379578,              prod3(                  154,                218,               195)             prod32(                       213,                201),             3                 prod4(130,                                85,                 134,               84),                    min22(                14,12)        ,     min1(                                  496),                   max73(250302336,                                                             3044, 6)                           prod2(                  44,             greater2(
'''
def update_closing_brackets(clsb, bits, pkgs=1):
    for i, [type, value] in enumerate(clsb):
        if type == 'bits':
            clsb[i][1] -= bits
    if clsb and clsb[-1][0] == 'pkgs':
        clsb[-1][1] -= pkgs
    return clsb


def iterate_operation(b):
    expression = ''
    closing_brackets = []  # keep track of opening and closing brackets
    while '1' in b:
        version = int(b[:3], 2)
        typeid = int(b[3:6], 2)
        if typeid == 4:
            literbit = ''
            start_bit = 6
            while b[start_bit] == '1':
                literbit += b[start_bit+1:start_bit+5]
                start_bit += 5
            literbit += b[start_bit+1:start_bit+5]
            expression += (str(int(literbit, 2)) + ',')

            closing_brackets = update_closing_brackets(closing_brackets, bits=start_bit+5)
            b = b[(start_bit+5):]
        else:
            operation = typeid_ops[typeid]
            length_type_id = b[6]
            if length_type_id == '0':
                total_bit_length = int(b[7:22], 2)
                expression += operation
                closing_brackets = update_closing_brackets(closing_brackets, bits=22)
                closing_brackets.append(['bits', total_bit_length])
                b = b[22:]
            else:
                subpacket_number = int(b[7:18], 2)
                expression += operation
                closing_brackets = update_closing_brackets(closing_brackets, bits=18)
                closing_brackets.append(['pkgs', subpacket_number])
                b = b[18:]
        while closing_brackets and closing_brackets[-1][1] == 0:
            expression += '])'
            closing_brackets.pop()
            if closing_brackets:
                expression += ','
    return expression
        

def part2_solution(b):
    return eval(iterate_operation(b))


if __name__ == "__main__":
    for inp, outp in tests.items():
        expected_result = recursive_read(hex_to_bin(inp))
        if expected_result != outp:
            print(inp, expected_result, outp)
            break
    with open('2021/day16.txt', 'r') as f:
        hex = f.readline()
    binary = hex_to_bin(hex)
    print(part1_solution(binary))
    print(part2_solution(binary))