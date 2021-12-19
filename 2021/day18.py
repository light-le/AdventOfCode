'''
[[[7,[8,[3,5]]],[[[3,6],9],1]],[[[[1,7],8],[0,4]],[[[0,9],2],[2,[5,6]]]]]
[[[7,[11,0]],[[[8,6],9],1]],[[[[1,7],8],[0,4]],[[[0,9],2],[2,[5,6]]]]]
[[[7,[11,8]],[[0,15],1]],[[[[1,7],8],[0,4]],[[[0,9],2],[2,[5,6]]]]]
[[[7,[11,8]],[[0,15],2]],[[[0,15],[0,4]],[[[0,9],2],[2,[5,6]]]]]
[[[7,[11,8]],[[0,15],2]],[[[0,15],[0,4]],[[0,11],[2,[5,6]]]]]
[[[7,[11,8]],[[0,15],2]],[[[0,15],[0,4]],[[0,11],[7,0]]]]

[[[12,[0,14]],[[0,15],2]],[[[0,15],[0,4]],[[0,11],[7,0]]]]
[[[[6,6],[7,0]],[[7,15],2]], [[[0,15],[0,4]],[[0,11],[7,0]]]]
[[[[6,6],[7,0]],[[14,0],10]], [[[0,15],[0,4]],[[0,11],[7,0]]]]
[[[[6,6],[7,7]],[[0,7],[5,5]]], [[[0,15],[0,4]],[[0,11],[7,0]]]]
[[[[6,6],[7,7]],[[0,7],[5,5]]], [[[7,0],[8,4]],[[5,6],[0,7]]]]



[[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]] , [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]
[[[[4,0],[5,4]],[[7,0],[15,5]]] , [10,[[11,9],[11,0]]]]
[[[[4,0],[5,4]],[[7,7],[6,0]]] , [17,[[11,9],[11,0]]]]
[[[[4,0],[5,4]],[[7,7],[6,0]]] , [[8,[7,7]],[[7,9],[5,0]]]]

[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]


            [[6,[5,[4,[3,2]]]],1]
[6,[5,[4,[3,2]]]]                    1
6           [5,[4,[3,2]]]               1
6           5           [4,[3,2]]           1
6           5           4       [3,2]       1

            [[[[[4,5],[2,6]],[9,5]]],2],3]
[[[[4,5],[2,6]],[9,5]]],2]              3
[[[4,5],[2,6]],[9,5]]]          2                   3
[[4,5],[2,6]]       [9,5]       2                   3
[4,5]       [2,6]       [9,5]  
'''
from functools import reduce
from math import ceil, floor

test_input = [
    '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
    '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
    '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
    '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
    '[7,[5,[[3,8],[1,4]]]]',
    '[[2,[2,2]],[8,[8,1]]]',
    '[2,9]',
    '[1,[[[9,3],9],[[9,0],[0,7]]]]',
    '[[[5,[7,4]],7],1]',
    '[[[[4,2],2],6],[8,7]]',
]
test_output = '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'

class SnailFish:
    def __init__(self, left, right, level=0) -> None:
        self.left = int(left) if left.isnumeric() else left
        self.right = int(right) if right.isnumeric() else right
        self._level = level
        self.parent = None
        self.isleftchild = None
    
    @property
    def level(self):
        return self._level
    @level.setter
    def level(self, lv):
        self._level = lv
        if isinstance(self.left, SnailFish):
            self.left.level = lv+1
        if isinstance(self.right, SnailFish):
            self.right.level = lv+1

    def __eq__(self, o):
        return str(self) == str(o)
    def __repr__(self) -> str:
        return f'[{self.left},{self.right}]'

    def add(self, o):
        self.level +=1
        o.level += 1
        
        parent_fish = SnailFish(self, o)
        
        self.parent = parent_fish
        self.isleftchild = True
        
        o.parent = parent_fish
        o.isleftchild = False
        return parent_fish


    def isnumeric(self):
        return False

    def add_parent(self):
        if isinstance(self.left, SnailFish):
            self.left.parent = self
            self.left.isleftchild = True
            self.left.add_parent()
        if isinstance(self.right, SnailFish):
            self.right.parent = self
            self.right.isleftchild = False
            self.right.add_parent()
        return self
    
    def explode(self):
        left_exp = self.left
        right_exp = self.right
        if self.isleftchild:
            # add the right number to the right sibling of the parent
            if isinstance(self.parent.right, SnailFish):
                self.parent.right.left += right_exp
            else:
                self.parent.right += right_exp
            # for the left number, climb up until you find yourself being right child
            climb_self = self
            while climb_self.parent and climb_self.parent.isleftchild:
                climb_self = climb_self.parent
            # either right child or at root
            if climb_self.parent and climb_self.parent.isleftchild == False:
                # add the left number to the rightmost children
                climb_self = climb_self.parent.parent
                if isinstance(climb_self.left, SnailFish):
                    climb_self = climb_self.left
                    while isinstance(climb_self.right, SnailFish):
                        climb_self = climb_self.right
                    climb_self.right += left_exp
                else:
                    climb_self.left += left_exp
            # unlink
            self.parent.left = 0
        else:
            if isinstance(self.parent.left, SnailFish):
                self.parent.left.right += left_exp
            else:
                self.parent.left += left_exp
            climb_self = self
            while climb_self.parent and not climb_self.parent.isleftchild:
                climb_self = climb_self.parent
            if climb_self.parent and climb_self.parent.isleftchild:
                climb_self = climb_self.parent.parent
                if isinstance(climb_self.right, SnailFish):
                    climb_self = climb_self.right
                    while isinstance(climb_self.left, SnailFish):
                        climb_self = climb_self.left
                    climb_self.left += right_exp
                else:
                    climb_self.right += right_exp
            # unlink
            self.parent.right = 0
        self = 0


    def explode_detect(self):
        '''
        check if level 4, then explode
        '''
        if self.level == 4:
            self.explode()
        if isinstance(self.left, SnailFish):
            self.left.explode_detect()
        if isinstance(self.right, SnailFish):
            self.right.explode_detect()

    def split(self, left_half, right_half):
        if not isinstance(self.left, SnailFish) and self.left == (left_half + right_half):
            self.left = SnailFish(str(left_half), str(right_half), self.level+1)
            self.left.parent = self
            self.left.isleftchild = True
        else:
            self.right = SnailFish(str(left_half), str(right_half), self.level+1)
            self.right.parent = self
            self.right.isleftchild = False

    def split_detect(self):
        '''
        check if any of the children has integer 10 or above, stop and return true at first sight
        '''
        if isinstance(self.left, SnailFish):
            result = self.left.split_detect()
            if result:
                return True
        else:
            if self.left >= 10:
                self.split(floor(self.left/2), ceil(self.left/2))
                return True
        if isinstance(self.right, SnailFish):
            result = self.right.split_detect()
            if result:
                return True
        else:
            if self.right >= 10:
                self.split(floor(self.right/2), ceil(self.right/2))
                return True

    def print_all_levels(self):
        print(self, self.level)
        if isinstance(self.left, SnailFish):
            self.left.print_all_levels()
        if isinstance(self.right, SnailFish):
            self.right.print_all_levels()

    def magnitude_sum(self):
        if isinstance(self.left, int) and isinstance(self.right, int):
            return 3*self.left+2*self.right
        elif isinstance(self.left, int):
            return 3*self.left+2*self.right.magnitude_sum()
        elif isinstance(self.right, int):
            return 3*self.left.magnitude_sum()+2*self.right
        return 3*self.left.magnitude_sum() + 2*self.right.magnitude_sum()


def recursive_parser(snf, level=0):
    snf_no_outer_brackets = snf[1:-1]
    if snf_no_outer_brackets[0].isnumeric() and snf_no_outer_brackets[-1].isnumeric():
        left, right = snf_no_outer_brackets.split(',')
        return SnailFish(left, right, level)
    
    if snf_no_outer_brackets[0] == '[':
        # search for the matching closing braket
        opening_brackets = 0
        for c, char in enumerate(snf_no_outer_brackets):
            if char == '[':
                opening_brackets += 1
            elif char == ']':
                opening_brackets -= 1
            if opening_brackets == 0:
                break
        
        left = snf_no_outer_brackets[:c+1]
        right = snf_no_outer_brackets[c+2:]
        if right.isnumeric():
            return SnailFish(recursive_parser(left, level+1), right, level)
        else:
            return SnailFish(recursive_parser(left, level+1), recursive_parser(right, level+1), level)
    else:
        # search for the first opening bracket
        opening_i = snf_no_outer_brackets.index('[')
        left = snf_no_outer_brackets[:opening_i-1]
        right = snf_no_outer_brackets[opening_i:]
        return SnailFish(left, recursive_parser(right, level+1))
            
def add_explode_split(fa, fb):
    fs = fa.add(fb)
    fs.explode_detect()
    while fs.split_detect():
        fs.explode_detect()
    return fs

def add_all_fishes(strli):
    fish_schools = [recursive_parser(fish).add_parent() for fish in strli]
    final_fishes = reduce((lambda a, b: add_explode_split(a, b)), fish_schools)
    return final_fishes

def part1_solution(strli):
    final_fishes = add_all_fishes(strli)
    return final_fishes.magnitude_sum()

def test_run_part1(inp, outp):
    cal_outp = add_all_fishes(inp)
    return outp == str(cal_outp)

def part2_solution(fish_strli):
    max_mag = 0
    for fishschool1 in fish_strli:
        for fishschool2 in fish_strli:
            if fishschool1 == fishschool2:
                continue
            fishschool3 = add_explode_split(recursive_parser(fishschool1).add_parent(),
                                            recursive_parser(fishschool2).add_parent())
            max_mag = max(max_mag, fishschool3.magnitude_sum())
    return max_mag
if __name__ == "__main__":

    assert test_run_part1(test_input, test_output)
    with open('2021/day18.txt', 'r') as f:
        li = f.read().rsplit()

    print(part1_solution(li))
    print(part2_solution(li))