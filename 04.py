class Board():
    def __init__(self, lines):
        rows = [[int(x) for x in line.strip().replace("  ", " ").split(" ")] for line in lines]
        cols = [ [] for line in lines]
        for i in range(5):
            for j in range(5):
                cols[i].append(rows[j][i])

        self.rows = list(map(lambda x: set(x), rows))
        self.cols = list(map(lambda x: set(x), cols))

    def call(self, num):
        # Remove a number && handle end-game
        for i, row in enumerate(self.rows):
            row.discard(num)
            self.cols[i].discard(num)

        if not all(map(len, self.rows + self.cols)): # override len=0 ~ False
                sum_left = sum([sum(row) for row in self.rows])
                return sum_left*num
        else:
                return None

if __name__ == "__main__":
    import sys
    boards = set()
    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
        draw = lines.pop(0)
        while lines:
            lines.pop(0) # blank
            boards.add(Board([lines.pop(0) for i in range(5)]))
    first_found = False
    for ball in draw.split(","):
        ball = int(ball)
        boards_to_delete = set()
        for board in boards:
            if (result := board.call(ball)) is not None:
                if not first_found:
                    print(result)
                    first_found = True
                boards_to_delete.add(board)
                if boards_to_delete == boards: # Last one
                    print(result)
                    exit(0)
        boards -= boards_to_delete

    print("No result")
