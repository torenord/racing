class Position:
    def __init__(self):
        initial = """
   +---+---+---+---+---+---+---+---+
 8 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 7 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 6 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 5 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 4 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 3 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 2 | k | r | b | n | N | B | R | K |
   +---+---+---+---+---+---+---+---+
 1 | q | r | b | n | N | B | R | Q |
   +---+---+---+---+---+---+---+---+
     a   b   c   d   e   f   g   h   █
"""

        self.parse(initial)

    def __repr__(self):
        turnmarker = "\u2588"

        s = "   +---+---+---+---+---+---+---+---+\n"

        for i in range(8):
            rank = 8-i
            s += " %s | " % rank + " | ".join(self.board[i]) + " |\n"
            s += "   +---+---+---+---+---+---+---+---+\n"

        s += " "
        s += turnmarker if not self.whitesTurn else " "
        s += "   a   b   c   d   e   f   g   h   "
        s += turnmarker if self.whitesTurn else ""

        return s

    def __str__(self):
        s = repr(self)

        colorsenabled = True

        def makered(s):
            if colorsenabled:
                return "\033[1m\033[91m" + s + "\033[0m"
            else:
                return s

        if colorsenabled:
            for blackpiece in "kqrbn":
                s = s.replace(blackpiece, makered(blackpiece))

        return s

    def parse(self, s):
        self.board = [row.strip()[4:-2].split(" | ") for row in s.strip().split("\n")[1:17:2]]
        self.whitesTurn = s.strip().split("\n")[-1][1] == " "

        return self

if __name__ == '__main__':
    from sys import stdin

    if not stdin.isatty():
        p = Position().parse(stdin.read())
        print(p)
