class BingoBoard:
    def __init__(self, board) -> None:
        self.board = board
        self.boarddict = self.list_to_dict()
        self.reset()

    def reset(self):
        self.markedx = {i: 0 for i in range(5)}
        self.markedy = {i: 0 for i in range(5)}
        self.markedsum = 0

    def mark_board(self, marker):
        if marker in self.boarddict:
            self.markedx[self.boarddict[marker][0]] += 1
            self.markedy[self.boarddict[marker][1]] += 1
            self.markedsum += marker
            return self.check_if_win(marker)
        return False

    def check_if_win(self, marker):
        if 5 in self.markedx.values() or 5 in self.markedy.values():
            return self.score(marker)
        else:
            return False

    def score(self, marker):
        total = sum([sum(row) for row in self.board])
        return (total - self.markedsum)*marker

    def list_to_dict(self):
        board_dict = dict()
        for x, row in enumerate(self.board):
            board_dict.update({int(num): (x, y) for y, num in enumerate(row)})
        return board_dict


def part1_solution(nums, boards):
    score = None
    for num in nums:
        for board in boards:
            score = board.mark_board(num)
            if score:
                return score

def part2_solution(nums, boards):
    winners = [False] * len(boards)
    for num in nums:
        for b, board in enumerate(boards):
            if not winners[b]:
                score = board.mark_board(num)
                if score:
                    winners[b] = True
                    if all(winners):
                        return score

if __name__ == "__main__":
    with open('2021/day4.txt') as f:
        lines = f.read().rsplit(sep='\n\n')
    
    drawer, *boards = lines
    nums = [int(n) for n in drawer.split(',')]

    binboards = [[[int(num) for num in row.split()] for row in board.rsplit(sep='\n')] for board in boards]
    
    boards = [BingoBoard(board) for board in binboards]
    print(part1_solution(nums, boards))
    [board.reset() for board in boards]
    print(part2_solution(nums, boards))