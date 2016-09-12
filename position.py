class Position:
    def parse(s):
        p = Position()

        p.board = [row.strip()[4:-2].split(" | ") for row in s.strip().split("\n")[1:17:2]]
        p.whitesTurn = s.strip().split("\n")[-1][1] == " "

        return p

    def __str__(self):
        colorsenabled = True
        turnmarker = "\u2588"

        def makered(s):
            if colorsenabled:
                return "\033[1m\033[91m" + s + "\033[0m"
            else:
                return s

        s = "   +---+---+---+---+---+---+---+---+\n"

        for i in range(8):
            rank = 8-i
            s += " %s | " % rank + " | ".join(self.board[i]) + " |\n"

            for blackpiece in "kqrbn":
                s = s.replace(blackpiece, makered(blackpiece))

            s += "   +---+---+---+---+---+---+---+---+\n"

        s += " "
        s += makered(turnmarker) if not self.whitesTurn else " "
        s += "   a   b   c   d   e   f   g   h   "
        s += turnmarker if self.whitesTurn else ""

        return s

if __name__ == '__main__':
    from sys import stdin

    if not stdin.isatty():
        p = Position.parse(stdin.read())
        print(p)
