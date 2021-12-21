from itertools import product
from collections import Counter

def quantum_dice_possible_sum_count(v=[1,2,3]):
    '''
    count the possible sums of 3 dice rolls
    for example 1,2,3 and 3,2,1 and 2,2,2 are 3 possiblilties but they have same sum
    '''
    possible_rolls = product(v, repeat=len(v))
    prod_sums = [sum(pr) for pr in possible_rolls]
    return dict(Counter(prod_sums))

def part1_solution(p1pos, p2pos):
    p1score = 0
    p2score = 0

    dice = [-2, -1, 0]
    dice_rolls = 0

    turn = 'p1'
    while p1score < 1000 and p2score < 1000:
        dice = [(d+3)% 10 for d in dice]
        dice_rolls += 3

        if turn == 'p1':
            p1pos = ((p1pos + sum(dice) - 1) % 10) + 1
            p1score += p1pos
            turn = 'p2'
        else:
            p2pos = ((p2pos + sum(dice) - 1) % 10) + 1
            p2score += p2pos
            turn = 'p1'
    if p1score > p2score:
        return p2score*dice_rolls
    else:
        return p1score*dice_rolls


def part2_solution(p1pos, p2pos):
    qdice_sums = quantum_dice_possible_sum_count()

    p1pos_possibilities = {
        ((p1pos+k-1)%10)+1: v for k,v in qdice_sums.items()
    }
    p1_posscore_possibilities = {(p, p): v for p, v in p1pos_possibilities.items()}
    
    p2pos_possibilities = {
        ((p2pos+k-1)%10)+1: v for k,v in qdice_sums.items()
    }
    p2_posscore_possibilities = {(p, p): v for p, v in p2pos_possibilities.items()}

    p1_win_possibilities = 0
    p2_win_possibilities = 0
    while p1_posscore_possibilities and p2_posscore_possibilities:
        p1_new_posscore_possibilities = dict()
        for (pos, score), possibilities in p1_posscore_possibilities.items():
            new_pos = [((pos+k-1)%10)+1 for k in qdice_sums]
            new_score = [score + pos for pos in new_pos]
            new_possibilities = [possibilities*v for v in qdice_sums.values()]
            
            for pos, score, poss in zip(new_pos, new_score, new_possibilities):
                if (pos, score) in p1_new_posscore_possibilities:
                    p1_new_posscore_possibilities[(pos, score)] += poss
                else:
                    p1_new_posscore_possibilities[(pos, score)] = poss

        p1_winning_posscore = {(pos, score): p for (pos, score), p in p1_new_posscore_possibilities.items() if score >= 21}
        p1_win_possibilities += (sum(p1_winning_posscore.values()) * sum(p2_posscore_possibilities.values()))

        p1_posscore_possibilities = {(pos, score): p for (pos, score), p in p1_new_posscore_possibilities.items() if score < 21}

        p2_new_posscore_possibilities = dict()
        for (pos, score), possibilities in p2_posscore_possibilities.items():
            new_pos = [((pos+k-1)%10)+1 for k in qdice_sums]
            new_score = [score + pos for pos in new_pos]
            new_possibilities = [possibilities*v for v in qdice_sums.values()]
            
            for pos, score, poss in zip(new_pos, new_score, new_possibilities):
                if (pos, score) in p2_new_posscore_possibilities:
                    p2_new_posscore_possibilities[(pos, score)] += poss
                else:
                    p2_new_posscore_possibilities[(pos, score)] = poss

        p2_winning_posscore = {(pos, score): p for (pos, score), p in p2_new_posscore_possibilities.items() if score >= 21}
        p2_win_possibilities += (sum(p2_winning_posscore.values()) * sum(p1_posscore_possibilities.values()))

        p2_posscore_possibilities = {(pos, score): p for (pos, score), p in p2_new_posscore_possibilities.items() if score < 21}

    return max(p1_win_possibilities, p2_win_possibilities)

if __name__ == "__main__":
    print(part1_solution(3, 5))
    print(part2_solution(3, 5))
