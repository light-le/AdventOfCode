
def find_lowest_bottoms(heights):
    low_heights = []
    # check every inner points (not the outer edges)
    for r, row in enumerate(heights):
        if r == 0 or r == (len(heights)-1):
            continue
        for c, col in enumerate(row):
            if c == 0 or c == (len(row)-1):
                continue
            surrounding_heights = [
                heights[r][c-1],
                heights[r][c+1],
                heights[r-1][c],
                heights[r+1][c],
            ]
            if all([col < h for h in surrounding_heights]):
                low_heights.append((r,c,col))
    
    # check the 4 corners: topleft, botton left, top right, bottom right
    if heights[0][0] < heights[0][1] and heights[0][0] < heights[1][0]:
        low_heights.append((0, 0, heights[0][0]))
    if heights[-1][0] < heights[-2][0] and heights[-1][0] < heights[-1][1]:
        low_heights.append((len(heights)-1, 0, heights[-1][0]))
    if heights[0][-1] < heights[0][-2] and heights[0][-1] < heights[1][-1]:
        low_heights.append((0, len(heights[0])-1, heights[0][-1]))
    if heights[-1][-1] < heights[-2][-1] and heights[-1][-1] < heights[-1][-2]:
        low_heights.append((len(heights)-1, len(heights[0])-1, heights[-1][-1]))

    # check the left right edges
    for c in range(1, len(heights[0])-1):
        surrounding_top = [
            heights[0][c-1],
            heights[0][c+1],
            heights[1][c],
        ]
        if all([heights[0][c] < h for h in surrounding_top]):
            low_heights.append((0, c, heights[0][c]))

        surrounding_bottom = [
            heights[-1][c-1],
            heights[-1][c+1],
            heights[-2][c],
        ]
        if all([heights[-1][c] < h for h in surrounding_bottom]):
            low_heights.append((len(heights)-1, c, heights[-1][c]))

    # check bottom edges
    for r in range(1, len(heights)-1):
        surrounding_left = [
            heights[r-1][0],
            heights[r+1][0],
            heights[r][1],
        ]
        if all([heights[r][0] < h for h in surrounding_left]):
            low_heights.append((r, 0, heights[r][0]))

        surrounding_right = [
            heights[r-1][-1],
            heights[r+1][-1],
            heights[r][-2],
        ]
        if all([heights[r][-1] < h for h in surrounding_right]):
            low_heights.append((r, len(heights[0])-1, heights[r][-1]))
    return low_heights
def part1_solution(low_heights):
    return sum([h[2] for h in low_heights]) + len(low_heights)

def can_add_to_frontier(pr, pc, h, heights, basin):
    if pr < 0 or pc < 0 or pr >= len(heights) or pc >= len(heights[0]):
        return False
    if (pr, pc) in basin:
        return False
    if heights[pr][pc] <= h:
        return False
    if heights[pr][pc] == 9:
        return False
    return True
    
def find_basin(r, c, h, heights):
    # DFS, FIFO
    frontier = [(r, c, h)]
    basin = [(r, c)]
    while frontier:
        pointr, pointc, pointh = frontier.pop(0)
        for sur_r, sur_c in [(pointr-1, pointc), (pointr+1, pointc), (pointr, pointc-1), (pointr, pointc+1)]:
            if can_add_to_frontier(sur_r, sur_c, pointh, heights, basin):
                frontier.append((sur_r, sur_c, heights[sur_r][sur_c]))
                basin.append((sur_r, sur_c))
    return len(basin)


def part2_solution(bottoms, heights):
    basins = [] # list of list of sizes
    for r, c, h in bottoms:
        basins.append(find_basin(r, c, h, heights))
    sorted_basins = sorted(basins, reverse=True)
    return sorted_basins[0] * sorted_basins[1] * sorted_basins[2]


if __name__ == "__main__":
    with open('2021/day9.txt', 'r') as f:
        cave = f.read().rsplit()
    heights = [[int(c) for c in row] for row in cave]
    low_heights = find_lowest_bottoms(heights)
    print(part1_solution(low_heights))
    print(part2_solution(low_heights, heights))