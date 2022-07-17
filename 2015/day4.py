from hashlib import md5

def mining(leading_zeros = 5, prefix='ckczppom'):
    hashed = ''
    c = 0
    while not hashed.startswith('0'*leading_zeros):
        c += 1
        combine = prefix + str(c)
        hashed = md5(combine.encode()).hexdigest()
    return c


if __name__ == '__main__':
    print('Part1', mining(5))
    print('Part2', mining(6))