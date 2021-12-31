#!/usr/bin/python
import sys

"""
Each stage of the MONAD program does the following,
with 3 different coefficients at each stage (c1,c2,c3).
calc_z(inp, last_z, c1, c2, c3):
    w = inp 
    x = last_z
    x %= 26
    z = last_z // c1
    x += c2
    x = 0 if x==w else 1
    y = 25
    y *= x
    y += 1
    z *= y
    y = w
    y += c3
    y *= x
    z += y
This simplifies down to the code in the calc_z() method below.
"""
def calc_z(inp, last_z, c1, c2, c3):
    z = last_z//c1
    #x = (last_z % 26) + c2
    #if x!=inp:
    if inp != last_z%26 + c2:
        z *= 26
        z += inp + c3
    #print(z, end=" ")
    return z

# From code-reading the input:
coeffs = [ (1,11,6),
           (1,11,12),
           (1,15,8),
           (26,-11,7),
           (1,15,7),
           (1,15,12),
           (1,14,2),
           (26,-7,15),
           (1,12,4),
           (26,-6,5),
           (26,-10,12),
           (26,-15,11),
           (26,-9,13),
           (26,0,7)
           ]

def final_z(inps):
    z = 0
    for i,inp in enumerate(inps):
        c1,c2,c3 = coeffs[i]
        z = calc_z(inp, z, c1,c2,c3)
    return z

# Either test a specific input, or else solve (both parts one and two)
if len(sys.argv) > 1:
    inps = [int(c) for c in sys.argv[1]]
    print(final_z(inps))
else:
    # To solve, note how the calc_z function interacts with the
    # coefficients we have.  For c1=1, c2 > 10, always.  That means
    # last_z%26 + c2 > 10 always, and so can never equal the input (1-9).
    # So at each c1=1 stage, z is multiplied by 26.  There are 7 of these
    # stages and 7 c1=26 stages, so we need every c1=26 stage to divide
    # by 26 to get down to 0 at the end.  That means each c1=26 stage must
    # not enter the branch.  That means choosing an input mN such that
    # m[N] = inp == z[N-1] + c2[N].
    #
    # z0 = m0 + 6 (we always enter the branch)
    # z1 = 26*z0 + m1 + 6
    # z2 = 26*z1 + m2 + 8
    # z3 = z2//26 = z1              IF m3 == m2+8-11 = m2 - 3
    # z4 = 26*z3 + m4 + 7
    # z5 = 26*z4 + m5 + 12
    # z6 = 26*z5 + m6 + 2
    # z7 = z6//26 = z5              IF m7 == m6+2-7 = m6 - 5
    # z8 = 26*z7 + m8 + 4
    # z9 = z8//26 = z7 = z5         IF m9 == m8+4-6 = m8 - 2
    # z10 = z9//26 = z4//26 = z3    IF m10 == m5+12-10 = m5 + 2
    # z11 = z10//26 = z4//26 = z1   IF m11 == m4+7-15 = m4 - 8
    # z12 = z11//26 = z0            IF m12 == m1+12-9 = m1 + 3
    # z13 = z12//26 = z0//26 = 0    IF m13 == m12%26+0 = z0 = m0 + 6
    #
    # This is now a constraints problem!
    from ortools.sat.python import cp_model

    def solve(biggest = True):
        model = cp_model.CpModel()
        ms = []
        for m in range(14):
            ms.append(model.NewIntVar(1,9, "m%d" %m))

        model.Add(ms[3] == ms[2] - 3)
        model.Add(ms[7] == ms[6] - 5)
        model.Add(ms[9] == ms[8] - 2)
        model.Add(ms[10] == ms[5] + 2)
        model.Add(ms[11] == ms[4] - 8)
        model.Add(ms[12] == ms[1] + 3)
        model.Add(ms[13] == ms[0] + 6)

        fun = model.Maximize if biggest else model.Minimize
        fun(ms[0]*10**13 + \
                   ms[1]*10**12 + \
                   ms[2]*10**11 + \
                   ms[3]*10**10 + \
                   ms[4]*10**9 + \
                   ms[5]*10**8 + \
                   ms[6]*10**7 + \
                   ms[7]*10**6 + \
                   ms[8]*10**5 + \
                   ms[9]*10**4 + \
                   ms[10]*10**3 + \
                   ms[11]*10**2 + \
                   ms[12]*10 + \
                   ms[13])
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        #print(status, solver.Value(ms[0]), solver.NumBranches())
        inps = [solver.Value(m) for m in ms]
        print("".join([str(x) for x in inps]), "->", final_z(inps))

    solve(True)
    solve(False)
