from position import Position
from search import negamax
import readline
import sys
import time

inf = 1000

# Initial game position
position = Position().setup()

# Principle variation
line = []

def decode(s):
    x = ord(s[0]) - ord("a")
    y = 8 - int(s[1])

    return x, y

def handle(cmd):
    global position
    global line

    # Quit
    if cmd == "q":
        exit()

    # Help
    if cmd == "h":
        print("q -- Quit")
        print("h -- Help")
        print("p -- Print current position")
        print("l -- Load position from file")
        print("s -- Save position to file")
        print("n -- Print legal next positions")
        print("c -- Compute to depth and apply best")
        print("t -- Compute in time and apply best")
        print("m -- Move a piece")
        print("v -- Show last principle variation")

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

    # Compute to depth and apply next positions
    elif cmd.split(" ")[0] == "c":
        try:
            start = time.time()
            depth = int(cmd.split(" ")[1])
            global line
            result = negamax(position, depth, -inf, inf)
            score = result["score"]
            line = result["line"]
            position = line[0]
            score *= -1 if position.whitesTurn else 1
            print(position)
            print("Evaluation: {0:.3}".format(score))
            end = time.time()
            print("Completed in {0:.3} seconds.".format(end - start))
        except (IndexError, ValueError):
            pass

    # Compute in time and apply next positions
    elif cmd.split(" ")[0] == "t":
        try:
            start = time.time()
            t = float(cmd.split(" ")[1])
            depth = 0
            while depth == 0 or time.time() - start < t:
                depth += 1
                result = negamax(position, depth, -inf, inf)
            score = result["score"]
            line = result["line"]
            position = line[0]
            score *= -1 if position.whitesTurn else 1
            print(position)
            print("Depth:", depth)
            print("Evaluation: {0:.3}".format(score))
            end = time.time()
            print("Completed in {0:.3} seconds.".format(end - start))
        except (IndexError, ValueError):
            pass

    # Move a piece
    elif cmd.split(" ")[0] == "m":
        a = cmd.split(" ")[1]
        b = cmd.split(" ")[2]

        y1, x1 = decode(a)
        y2, x2 = decode(b)

        position.movepiece(x1, y1, x2, y2)
        position.whitesTurn = not position.whitesTurn
        print(position)

    # Show last principles variation
    elif cmd.split(" ")[0] == "v":
        for p in line:
            print(p)

def do(gui_position):
    if len(sys.argv) == 2:
        for cmd in sys.argv[1].split(";"):
            handle(cmd.strip())
    else:
        while True:
            try:
                cmds = input("> ")
            except (EOFError, KeyboardInterrupt):
                print()
                break

            for cmd in cmds.split(";"):
                for i in range(8):
                    for j in range(8):
                        position.board[i][j] = gui_position.board[i][j]
                        position.whitesTurn = gui_position.whitesTurn
                handle(cmd.strip())
                for i in range(8):
                    for j in range(8):
                        gui_position.board[i][j] = position.board[i][j]
                        gui_position.whitesTurn = position.whitesTurn

if __name__ == '__main__':
    do(Position().setup())
