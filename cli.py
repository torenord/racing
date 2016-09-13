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

    # Print current position
    elif inp == "p":
        print(position)

    # Load position from file
    elif inp.split(" ")[0] == "l":
        filename = inp.split(" ")[1]
        position = Position().parse(open(filename).read())
        print(position)

    # Save position from file
    elif inp.split(" ")[0] == "s":
        filename = inp.split(" ")[1]
        with open(filename, "w") as f:
            f.write(repr(position))

    # Print legal next positions
    elif inp == "n":
        for p in position.legalmoves():
            print(p)
