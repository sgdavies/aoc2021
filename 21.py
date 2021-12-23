#!/usr/bin/python

ps = [4, 8] # test
ps = [7, 10] # data

class Die():
    def __init__(self):
        self.d = 1

    def roll_three(self):
        return self.roll() + self.roll() + self.roll()

    def roll(self):
        r = self.d
        self.d += 1
        if self.d > 100: self.d = 1
        return r

die = Die()
scores = [0, 0]
turn = 0

while True:
    player = turn%2
    turn += 1
    
    ps[player] += die.roll_three()
    while ps[player] > 10: ps[player] -= 10
    scores[player] += ps[player]

    if scores[player] >= 1000:
        print(3*turn*min(scores))
        break

# Part two
# {D,D,D} = 1x3, 3x4, 6x5, 7x6, 6x7, 3x8, 1x9
win_universes = [0,0]
def turn(positions, scores, player, universes):
    for rolls in [(1,3), (3,4), (6,5), (7,6), (6,7), (3,8), (1,9)]:
        new_scores = [scores[0], scores[1]]
        new_pos = [positions[0], positions[1]]
        n, d = rolls
        new_pos[player] += d
        if new_pos[player] > 10: new_pos[player] -= 10
        new_scores[player] += new_pos[player]
        if new_scores[player] >= 21:
            win_universes[player] += n*universes
        else:
            turn(new_pos, new_scores, (player+1)%2, n*universes)

turn([7,10], [0,0], 0, 1)
print(win_universes)
