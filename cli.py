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
    elif inp == "p":
        print(position)
