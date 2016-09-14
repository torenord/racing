from position import Position
from search import negamaxpos
import readline
import sys

# Initial game position
position = Position().setup()

def handle(cmd):
    global position

    # Quit
    if cmd == "q":
        exit()

    # Help
    if cmd == "h":
        print("q -- Quit")
        print("h -- Help")
        print("p -- Print current position")
        print("l -- Load position from file")
        print("s -- Save position from file")
        print("n -- Print legal next positions")
        print("c -- Compute and apply next positions")

    # Print current position
    elif cmd == "p":
        print(position)

    # Load position from file
    elif cmd.split(" ")[0] == "l":
        try:
            filename = cmd.split(" ")[1]
            position = Position().parse(open(filename).read())
            print(position)
        except (IndexError, ValueError):
            pass

    # Save position from file
    elif cmd.split(" ")[0] == "s":
        try:
            filename = cmd.split(" ")[1]
            with open(filename, "w") as f:
                f.write(repr(position))
        except (IndexError, ValueError):
            pass

    # Print legal next positions
    elif cmd == "n":
        for p in position.legalmoves():
            print(p)

    # Compute and apply next positions
    elif cmd.split(" ")[0] == "c":
        try:
            depth = int(cmd.split(" ")[1])
            p = negamaxpos(position, depth, -1000, 1000)
            print(p)
            position = p
        except (IndexError, ValueError):
            pass

if len(sys.argv) == 2:
    handle(sys.argv[1])
else:
    while True:
        try:
            cmd = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        handle(cmd)
