#!/usr/bin/python

# Each spot on the map is labelled
# Hall 0-10
# 01234567890
# ..*.*.*.*..
#  1.3.5.7.   Rooms 11-18
#  2.4.6.8. 
#
# A's room 11,12 ; B 13,14 ; C 15,16 ; D 17,18
# Doors (hall spots outside rooms) (*) are A:2, B:4, C:6, D:8
ROOMS = [ [11,12,13,14], [11,12,13,14], [11,12,13,14], [11,12,13,14], # A
          [15,16,17,18], [15,16,17,18], [15,16,17,18], [15,16,17,18], # B
          [19,20,21,22], [19,20,21,22], [19,20,21,22], [19,20,21,22], # C
          [23,24,25,26], [23,24,25,26], [23,24,25,26], [23,24,25,26], # D
        ]
DOOR_FOR_POD = [2,2,2,2, 4,4,4,4, 6,6,6,6, 8,8,8,8]
DOOR_FOR_ROOM = {11:2, 12:2, 13:2, 14:2,
                 15:4, 16:4, 17:4, 18:4,
                 19:6, 20:6, 21:6, 22:6,
                 23:8, 24:8, 25:8, 26:8}
FIRST_FOR_ROOM = {11:11, 12:11, 13:11, 14:11,
                  15:15, 16:15, 17:15, 18:15,
                  19:19, 20:19, 21:19, 22:19,
                  23:23, 24:23, 25:23, 26:23}
HALL_END = 10

start_positions = [11,12,13,14, 15,16,17,18, 19,20,21,22, 23,24,25,26]  # Solved position
start_positions = [19,12,13,14, 15,16,17,18, 11,20,21,22, 23,24,25,26]  # 
start_positions = [23,12,13,14, 15,16,17,18, 19,20,21,22, 11,24,25,26]  # 
start_positions = [14,21,24,26, 11,17,19,20, 15,16,22,25, 12,13,18,23]  # Test positions
start_positions = [15,18,21,24, 11,19,17,20, 23,26,16,25, 14,22,12,13]  # Real positions
N = len(start_positions)

from typing import NamedTuple
class Move(NamedTuple):
    pod: int
    old: int
    new: int
    steps: int

class CanonicalPosition(NamedTuple):
    a1: int
    a2: int
    a3: int
    a4: int
    b1: int
    b2: int
    b3: int
    b4: int
    c1: int
    c2: int
    c3: int
    c4: int
    d1: int
    d2: int
    d3: int
    d4: int

best = None
n_best = None
best_moves = None

# Do the passed-in move; evaluate (either end or dig deeper); then undo and return
# Caller gets back pod positions, stack unchanged (so can move onto next iteration)
def do_move(pods, move, stack, total_score, previous_states, depth):
    global best
    global n_best
    global best_moves

    # do move
    if move is not None:
        score = move.steps * 10**(move.pod//4)
        stack.append(move)
        pods[move.pod] = move.new
        total_score += score

        a1,a2,a3,a4 = sorted([pods[0], pods[1], pods[2], pods[3]])
        b1,b2,b3,b4 = sorted([pods[4], pods[5], pods[6], pods[7]])
        c1,c2,c3,c4 = sorted([pods[8], pods[9], pods[10], pods[11]])
        d1,d2,d3,d4 = sorted([pods[12], pods[13], pods[14], pods[15]])
        pos = CanonicalPosition(a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4)
        if pos in previous_states and total_score >= previous_states[pos]:
            # We've got to a previous position faster already - don't continue down this branch
            total_score -= score
            pods[move.pod] = move.old
            stack.pop()
            return
        else:
            previous_states[pos] = total_score
    #print(pods, move, depth)

    # if win: check score, undo move, return
    if all([pods[i] in ROOMS[i] for i in range(N)]):
        if best is None or total_score < best:
            best = total_score
            n_best = 1
            best_moves = stack.copy()
            print("Got a best:", best)
        elif total_score == best:
            n_best += 1

        if move is not None:
            stack.pop()
            pods[move.pod] = move.old
            total_score -= score
        return

    # for amphipod in pods:
    for pod in range(N):
        moves = []

        if pods[pod] <= HALL_END:
            # in the hall, you can only move back to your own room, and only then
            # if there are no different pods already in there, and only then if
            # there are no other pods in the hall blocking your route
            door = DOOR_FOR_POD[pod]
            if pods[pod] < door and any([hall in pods for hall in range(pods[pod]+1,door)]):
                # We're left of our door, but are blocked from reaching it
                #print("can't reach door from L", door,pod,pods[pod])
                pass
            elif any([hall in pods for hall in range(door+1, pods[pod])]):
                # We're to the right of our door, but are blocked from reaching it
                #print("can't reach door from R", door,pod,pods[pod])
                pass
            else:
                dest = None
                for room in ROOMS[pod]:
                    if room not in pods:
                        dest = room  # Deepest empty room
                    elif pods.index(room)//4 != pod//4:
                        # Someone else is in our room
                        dest = None
                        break
                if dest is not None:
                    moves.append(Move(pod, pods[pod], dest, abs(door-pods[pod])+1+dest-ROOMS[pod][0]))
        else:
            # In a room - either our own or someone else's
            if pods[pod] in ROOMS[pod] and all([pods.index(room)//4 == pod//4 for room in range(pods[pod]+1, ROOMS[pod][3]+1) ]):
                # We're in the right room, and so is everyone below us - none of us should move again
                pass
            elif any([room in pods for room in range(FIRST_FOR_ROOM[pods[pod]], pods[pod]) ]):
                # We're in the bottom of a room and we're blocked from getting out
                pass
            else:
                # We're in a room and can move out to the hall
                to_door = 1 + pods[pod] - FIRST_FOR_ROOM[pods[pod]]
                door = DOOR_FOR_ROOM[pods[pod]]
                for hall in range(door-1, -1, -1):  # from room left of door down to 0
                    if hall in DOOR_FOR_POD: continue  # Can't stop in a doorway
                    if hall in pods: break  # Blocked - can't stop here, or further along the hall 
                    moves.append(Move(pod, pods[pod], hall, to_door + door - hall))

                for hall in range(door+1, HALL_END+1):
                    if hall in DOOR_FOR_POD: continue  # Can't stop in a doorway
                    if hall in pods: break # Blocked - can't stop here, or further along the hall 
                    moves.append(Move(pod, pods[pod], hall, to_door + hall - door))

        for new_move in moves:
            do_move(pods, new_move, stack, total_score, previous_states, depth+1)

    # undo move & return
    if move is not None:
        stack.pop()
        pods[move.pod] = move.old
        total_score -= score
    #print("Done moves", pods)
    return

print(start_positions)
try:
    do_move(start_positions, None, [], 0, {}, 0)
except KeyboardInterrupt:
    print("You told be to stop")
print(best, n_best)
for move in best_moves:
    print(move)
