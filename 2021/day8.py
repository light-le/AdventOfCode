from functools import reduce

def part1_solution(notes):
    unique_nums = 0
    for ins, outs in notes:
        segments = outs.split(' ')
        seg_count = [len(seg) for seg in segments]
        unique_nums += (seg_count.count(2) + seg_count.count(3) + seg_count.count(4) + seg_count.count(7))
    return unique_nums

def part2_solution(notes):
    def intersect(a, b):
        '''
        return the number of common letters of a and b
        '''
        return len(set(a) & set(b))
    outnum = 0
    for ins, outs in notes:
        unique_segments = ins.split(' ')
        segment_count = [len(seg) for seg in unique_segments]
        segment_map = {
            1: unique_segments[segment_count.index(2)],
            4: unique_segments[segment_count.index(4)],
            7: unique_segments[segment_count.index(3)],
            8: unique_segments[segment_count.index(7)],
        }
        
        zero_six_nine = [s for s in unique_segments if len(s) == 6]
        segment_map[9] = [s for s in zero_six_nine if intersect(s, segment_map[4]) == 4][0]
        zero_six = [s for s in zero_six_nine if s != segment_map[9]]
        segment_map[0] = [s for s in zero_six if intersect(s, segment_map[1]) == 2][0]
        segment_map[6] = [s for s in zero_six if s != segment_map[0]][0]

        two_three_five = [s for s in unique_segments if len(s) == 5]
        segment_map[3] = [s for s in two_three_five if intersect(s, segment_map[1]) == 2][0]
        two_five = [s for s in two_three_five if s != segment_map[3]]
        segment_map[5] = [s for s in two_five if intersect(s, segment_map[4]) == 3][0]
        segment_map[2] = [s for s in two_five if s != segment_map[5]][0]

        in_out_mapping = {''.join(sorted(v)):str(k) for k,v in segment_map.items()}
        outnum += int(reduce((lambda a, b: a+b), [in_out_mapping[''.join(sorted(l))] for l in outs.split(' ')]))
    return outnum


if __name__ == "__main__":
    with open('2021/day8.txt', 'r') as f:
        notes = f.readlines()

    clean_notes = [note.rstrip().split(' | ') for note in notes]
    print(part1_solution(clean_notes))
    print(part2_solution(clean_notes))