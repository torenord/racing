import readline
from position import Position

# Initial game position
position = Position()

while True:
    try:
        inp = input("> ")
    except (EOFError, KeyboardInterrupt):
        print()
        break

    if inp == "q":
        break

    if inp == "h":
        print("q -- Quit")
        print("h -- Help")
        print("p -- Print current position")
        print("l -- Load position from file")
        print("s -- Save position from file")
        print("h -- Print legal next positions")

    # Print current position
    elif inp == "p":
        print(position)

    # Load position from file
    elif inp.split(" ")[0] == "l":
        try:
            filename = inp.split(" ")[1]
            position = Position().parse(open(filename).read())
            print(position)
        except:
            pass

    # Save position from file
    elif inp.split(" ")[0] == "s":
        try:
            filename = inp.split(" ")[1]
            with open(filename, "w") as f:
                f.write(repr(position))
        except:
            pass

    # Print legal next positions
    elif inp == "n":
        for p in position.legalmoves():
            print(p)
