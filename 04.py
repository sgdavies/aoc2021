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
                print("%d (%d, %d)" %(sum_left*num, num, sum_left))
                exit(0)

if __name__ == "__main__":
    import sys
    boards = []
    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
        draw = lines.pop(0)
        while lines:
            lines.pop(0) # blank
            boards.append(Board([lines.pop(0) for i in range(5)]))
    for ball in draw.split(","):
        ball = int(ball)
        for board in boards: board.call(ball)

    print("No result")
