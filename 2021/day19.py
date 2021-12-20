from math import pi, sin, cos

def rotation_matrix24():
    '''
    return 24 unique orthogonal rotational matrices
    '''
    rmat = []

    ortho_angles = [0, pi/2, pi, 3*pi/2]

    for pitch in ortho_angles:
        for roll in ortho_angles:
            for yaw in ortho_angles:
                rm = ((cos(pitch)*cos(roll), cos(pitch)*sin(roll)*sin(yaw)-sin(pitch)*cos(yaw), cos(pitch)*sin(roll)*cos(yaw)+sin(pitch)*sin(yaw)),
                      (sin(pitch)*cos(roll), sin(pitch)*sin(roll)*sin(yaw)+cos(pitch)*cos(yaw), sin(pitch)*sin(roll)*cos(yaw)-cos(pitch)*sin(yaw)),
                      (-sin(roll)          , cos(roll)*sin(yaw)                               , cos(roll)*cos(yaw)))
                rm = [[round(c) for c in row] for row in rm]
                if rm not in rmat:
                    rmat.append(rm)
    return rmat

def vector_multiply(a, b):
    '''
    basic 1xa * ax1 vectors, each of element muliply then sum
    '''
    return sum([aa*bb for aa, bb in zip(a,b)])

def check_12_matching(scannerpos, true_beacons, scanner_beacons):
    '''
    output true if at least 12 positions are matching between true beacons and scanner beacons
    '''
    scanner_beacons_translated = [[a+s for a, s in zip(scannerpos, sb)] for sb in scanner_beacons]
    common_beacons = [b for b in scanner_beacons_translated if b in true_beacons]
    return len(common_beacons) >= 12


def count_beacons_find_scanners(bcs):
    ortho_rmat = rotation_matrix24()
    scanner0, *other_scanners = bcs
    all_scanner_pos = []
    while other_scanners:
        scanner = other_scanners.pop(0) # FIFO
        absolute_scanner_pos = None
        for rmat in ortho_rmat:
            possible_scanner_pos = []
            rotated_scanner = [[vector_multiply(rm, s) for rm in rmat] for s in scanner]
            for abs_beacon in scanner0[:-11]:
                for rotated_beacon in rotated_scanner:
                    possible_pos = [a-s for a,s in zip(abs_beacon, rotated_beacon)]
                    if possible_pos in possible_scanner_pos and check_12_matching(possible_pos, scanner0, rotated_scanner):
                        absolute_scanner_pos = possible_pos
                        break
                    possible_scanner_pos.append(possible_pos)
                if absolute_scanner_pos:
                    break
            if absolute_scanner_pos:
                break
        if absolute_scanner_pos:
            transtated_beacons = [[a+s for a, s in zip(absolute_scanner_pos, sc)] for sc in rotated_scanner]
            all_scanner_pos.append(absolute_scanner_pos)
            for beacon in transtated_beacons:
                if beacon not in scanner0:
                    scanner0.append(beacon)
        else:
            other_scanners.append(scanner)
        print(len(scanner0), absolute_scanner_pos, len(other_scanners))
    return len(scanner0), all_scanner_pos

if __name__ == "__main__":
    with open('2021/day19.txt', 'r') as f:
        scanners = f.read().rsplit('\n\n')
    scanb = [s.split('\n') for s in  scanners]
    beacons = [[[int(c) for c in coord.split(',')] for coord in s[1:]] for s in scanb]

    beacons_count, scanner_pos = count_beacons_find_scanners(beacons)
    print(beacons_count)

    scanner_pos.append([0, 0, 0])
    max_mht_dist = 0
    for i in range(len(scanner_pos)-1):
        for j in range(i+1, len(scanner_pos)):
            scanner1 = scanner_pos[i]
            scanner2 = scanner_pos[j]
            mht_dist = sum([abs(sc1 - sc2) for sc1, sc2 in zip(scanner1, scanner2)])
            max_mht_dist = max(max_mht_dist, mht_dist)

    print(max_mht_dist)
