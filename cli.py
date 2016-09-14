from position import Position
import readline
import sys

# Initial game position
position = Position()

def handle(inp):
    global position

    # Quit
    if inp == "q":
        exit()

    # Help
    if inp == "h":
        print("q -- Quit")
        print("h -- Help")
        print("p -- Print current position")
        print("l -- Load position from file")
        print("s -- Save position from file")
        print("n -- Print legal next positions")
        print("c -- Compute and apply next positions")

    # Print current position
    elif inp == "p":
        print(position)

    # Load position from file
    elif inp.split(" ")[0] == "l":
        try:
            filename = inp.split(" ")[1]
            position = Position().parse(open(filename).read())
            print(position)
        except (IndexError, ValueError):
            pass

    # Save position from file
    elif inp.split(" ")[0] == "s":
        try:
            filename = inp.split(" ")[1]
            with open(filename, "w") as f:
                f.write(repr(position))
        except (IndexError, ValueError):
            pass

    # Print legal next positions
    elif inp == "n":
        for p in position.legalmoves():
            print(p)
if len(sys.argv) == 2:
    handle(sys.argv[1])
else:
    while True:
        try:
            inp = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        handle(inp)
