#!/usr/bin/python
import re,sys

def usage():
    print("python brainfuck.py [--optimize] <program|filename> [input-filename]")
    print("First argument will be opened as a file if possible, otherwise interpreted as a program")
    print("input-filename is optional - if you have input data, supply this (filename only)")

if len(sys.argv) < 2:
    usage()
    exit(1)

sys.argv.pop(0) # program name
first_arg = sys.argv.pop(0)
if first_arg == "--optimize":
    optimize = True
    prog_file = sys.argv.pop(0)
else:
    optimize = False
    prog_file = first_arg

try:
    with open(prog_file, 'r') as f:
        prog = f.read()
except:
    prog = prog_file

if sys.argv:
    with open(sys.argv.pop(), 'rb') as f:
        inputs = list(f.read())
else:
    inputs = ""

if optimize:
    oprog = ""
    for c in prog:
        if c in "<>+-[],.": oprog += c

    # [-] just sets current cell to 0
    oprog = oprog.replace("[-]","(0)")

    # Multiply : for cells {a, b*} and constant N, map to {a+b*N, 0*}
    # bf construction is [-<+++>] with N plusses
    # Naive optimization only matches for cell a immediately left of b
    # Matching right or not immediately adjacent would be possible but
    # trickier with the regex.
    mult = re.compile(r".*(\[-<(\++)>\]).*")
    while m := mult.match(oprog):
        group = m.group(1)
        group_loc = oprog.index(group)
        plusses = len(m.group(2))
        oprog = oprog[:group_loc] + "(*%d)"%plusses + oprog[group_loc+len(group):]

    prog = oprog
    #print("Optimized program:\n", prog)

tape = [0] * 1000  # Lazy (but prog will crash if this isn't sufficient, fail-fast FTW)

dp = 0
ip = 0
stack = []
out = []

while ip < len(prog):
  try:
    cmd = prog[ip]
    if cmd == '>': dp += 1
    elif cmd == '<': dp -= 1
    elif cmd == '+': tape[dp] += 1
    elif cmd == '-': tape[dp] -= 1
    elif cmd == '.': out.append(tape[dp])
    elif cmd == ',':
        if inputs:
            tape[dp] = inputs.pop(0)
        else: # EOF - leave unchanged
            pass
    elif cmd == '[':
        if tape[dp] == 0: # Skip to past matching ]
            depth = 1
            while depth > 0:
                ip += 1
                if prog[ip] == '[': depth += 1
                elif prog[ip] == ']': depth -= 1
        else: # We may jump back here later
            stack.append(ip)
    elif cmd == ']':
        jmp = stack.pop()
        if tape[dp] != 0: # Jump back
            ip = jmp -1 # -1 hack - gets corrected next
    elif optimize and cmd == '(':
        # Optimized instruction
        end_opt = ip+1
        while prog[end_opt] != ')': end_opt += 1
        opt_cmd = prog[ip+1:end_opt]
        ip = end_opt # Will continue after the optimized instruction
        if opt_cmd == "0":
            tape[dp] = 0
        elif opt_cmd[0] == "*":
            # For cells {a,b*} and value X -> {a+X*b, 0*}
            mult = int(opt_cmd[1:])
            tape[dp-1] += tape[dp]*mult
            tape[dp] = 0
        else:
            print("Invalid optimized command: '%s'" %opt_cmd)
            exit(1)
    else:
        pass

    ip += 1
  except BaseException as e:
      print("Error at this point in program:")
      print(ip)
      print(prog[ip-20:ip+1])
      raise e

print(" ".join([str(x) for x in out]))
#print("".join([chr(x) for x in out]))
