

filename = "looptest"

inp = open(filename+".fasm", "r")
out = open(filename+".hex", "w")
out.write("@0\n")

def printHex(binary):
    global out
    output = hex(binary)[2:].zfill(4)
    print(output)
    out.write(output[:2] + "\n")
    out.write(output[2:] + "\n")

while True:
    line = inp.readline()
    if not line:
        break

    line = line.split()

    if len(line) == 0 or len(line) == 1:
        continue

    data = line[1].split(',')
    instr = 0

    if line[0] == "sub":
        instr = 0b0000 << 12            # instruction
        instr += (int(data[1]) << 8)    # aaaa
        instr += (int(data[2]) << 4)    # bbbb
        instr += int(data[0])           # tttt
        printHex(instr)
    elif line[0] == "movl":
        instr = 0b1000 << 12            # instruction
        instr += (int(data[1]) << 4)    # literal value
        instr += int(data[0])           # reg number
        printHex(instr)
    elif line[0] == "movh":
        instr = 0b1001 << 12            # instruction
        instr += (int(data[1]) << 4)    # literal value
        instr += int(data[0])           # reg number
        printHex(instr)
    elif line[0] == "st":
        instr = 0b1111 << 12            # instruction
        instr += (int(data[1]) << 8)    # a
        instr += 0b0001 << 4
        instr += int(data[0])           # reg number
        printHex(instr)
    elif line[0] == "ld":
        instr = 0b1111 << 12            # instruction
        instr += (int(data[1]) << 8)    # a
        instr += 0b0000 << 4
        instr += int(data[0])           # reg number
        printHex(instr)

    elif line[0] in ["jz", "jnz", "js", "jns"]:
        instr = 0b1110 << 12            # instruction
        instr += (int(data[1]) << 8)    # a
        if line[0] == "jz":
            instr += 0b0000 << 4
        elif line[0] == "jnz":
            instr += 0b0001 << 4
        elif line[0] == "js":
            instr += 0b0010 << 4
        elif line[0] == "jns":
            instr += 0b0011 << 4
        else:
            print("err")
            exit(0)
        instr += int(data[0])           # reg number
        printHex(instr)

out.write("ff\nff\n")
inp.close()
out.close()