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
ROOMS = [ [11,12], [11,12], # A
          [13,14], [13,14], # B
          [15,16], [15,16], # C
          [17,18], [17,18], # D
        ]
DOOR_FOR_POD = [2,2, 4,4, 6,6, 8,8]
DOOR_FOR_ROOM = {11:2, 12:2, 13:4, 14:4, 15:6, 16:6, 17:8, 18:8}
HALL_END = 10

start_positions = [12,18, 11,15, 13,16, 14,17]  # Test positions
start_positions = [13,14, 11,15, 17,18, 12,16]  # Real positions
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
    b1: int
    b2: int
    c1: int
    c2: int
    d1: int
    d2: int

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
        score = move.steps * 10**(move.pod//2)
        stack.append(move)
        pods[move.pod] = move.new
        total_score += score

        a1,a2 = sorted([pods[0], pods[1]])
        b1,b2 = sorted([pods[2], pods[3]])
        c1,c2 = sorted([pods[4], pods[5]])
        d1,d2 = sorted([pods[6], pods[7]])
        pos = CanonicalPosition(a1,a2,b1,b2,c1,c2,d1,d2)
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
            #print("Got a best:", best)
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
            if pods[pod] < door and any([hall in pods for hall in range(pods[pod]+1,door)]): pass
            elif any([hall in pods for hall in range(door+1, pods[pod])]): pass
            elif ROOMS[pod][0] not in pods:  # There's a space in the room
                dist = abs(door - pods[pod])
                if ROOMS[pod][1] in pods:  # Who else is in the room?
                    who = pods.index(ROOMS[pod][1])
                    if who//2 == pod//2:
                        moves.append(Move(pod, pods[pod], ROOMS[pod][0], dist+1))
                    # else : someone else is in the room, so we're stuck
                else:
                    moves.append(Move(pod, pods[pod], ROOMS[pod][1], dist+2))
            # else : there's no space to move into
        else:
            # In a room - either our own or someone else's
            if pods[pod] == ROOMS[pod][1]:
                # We're in the bottom of our destination room - there's never a reason
                # to move out of here
                pass
            elif pods[pod] == ROOMS[pod][0] and pods.index(ROOMS[pod][1])//2 == pod//2:
                # We're at the top of our room, and our sibling is in the bottom of the room
                # - there's no reason to move either out at this point
                pass
            elif pods[pod]%2 == 0 and (pods[pod]-1) in pods:
                # We're in the bottom of a room and we're blocked from getting out
                pass
            else:
                # We're in a room and can move out to the hall
                to_door = 2 - pods[pod]%2
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

#print(start_positions)
try:
    do_move(start_positions, None, [], 0, {}, 0)
except KeyboardInterrupt:
    print("You told be to stop")
print(best, n_best)
#for move in best_moves:
#    print(move)
