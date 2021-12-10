import sys

def usage():
    print("python brainfuck.py <program|filename> [input-filename]")
    print("First argument will be opened as a file if possible, otherwise interpreted as a program")
    print("input-filename is optional - if you have input data, supply this (filename only)")

if len(sys.argv) < 2:
    usage()
    exit(1)

sys.argv.pop(0) # program name
first_arg = sys.argv.pop(0)
try:
    with open(first_arg, 'r') as f:
        prog = f.read()
except:
    prog = first_arg

if sys.argv:
    with open(sys.argv.pop(), 'rb') as f:
        inputs = list(f.read())
else:
    inputs = ""

tape = [0] * 10000

dp = 0
ip = 0
stack = []
out = ""

while ip < len(prog):
    cmd = prog[ip]
    if cmd == '>': dp += 1
    elif cmd == '<': dp -= 1
    elif cmd == '+': tape[dp] += 1
    elif cmd == '-': tape[dp] -= 1
    elif cmd == '.': out += chr(tape[dp])
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
    else:
        pass

    ip += 1

print(out)

