inf = 1000

class Position:
    def setup(self):
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
        return self

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
            lst = []
            for i in range(len(s.split("\n"))):
                line = s.split("\n")[i]
                if i < 2*8:
                    for blackpiece in "kqrbn":
                        line = line.replace(blackpiece, makered(blackpiece))
                lst.append(line)
            s = "\n".join(lst)

        return s

    def parse(self, s):
        self.board = [row.strip()[4:-2].split(" | ") for row in s.strip().split("\n")[1:17:2]]
        self.whitesTurn = s.strip().split("\n")[-1][1] == " "

        return self

    def validcell(self, i, j):
        return 0 <= i and i < 8 and 0 <= j and j < 8

    def emptycell(self, i, j):
        return self.board[i][j] == " "

    def opponentspiece(self, p):
        return p.islower() == self.whitesTurn

    def kingsymbol(self):
        return "K" if self.whitesTurn else "k"

    def knightsymbol(self):
        return "N" if self.whitesTurn else "n"

    def bishopsymbol(self):
        return "B" if self.whitesTurn else "b"

    def rooksymbol(self):
        return "R" if self.whitesTurn else "r"

    def queensymbol(self):
        return "Q" if self.whitesTurn else "q"

    def clone(self):
        p = Position()
        p.board = []
        for row in self.board:
            p.board.append(row[:])
        p.whitesTurn = self.whitesTurn
        return p

    def movepiece(self, x1, y1, x2, y2):
        self.board[x2][y2] = self.board[x1][y1]
        self.board[x1][y1] = " "

    def kingmoves(self):
        ret = []

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == self.kingsymbol():
                    kingmoves = [
                        (1,   1),
                        (1,   0),
                        (1,  -1),
                        (0,   1),
                        (0,  -1),
                        (-1,  1),
                        (-1,  0),
                        (-1, -1),
                    ]

                    for di, dy in kingmoves:
                        if self.validcell(i+di, j+dy):
                            if self.emptycell(i+di, j+dy) or self.opponentspiece(self.board[i+di][j+dy]):
                                p = self.clone()
                                p.movepiece(i, j, i+di, j+dy)
                                ret.append(p)

        return ret

    def knightmoves(self):
        ret = []

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == self.knightsymbol():
                    knightmoves = [
                        (2,  -1),
                        (2,   1),
                        (1,  -2),
                        (1,   2),
                        (-1, -2),
                        (-1,  2),
                        (-2, -1),
                        (-2,  1),
                    ]

                    for di, dy in knightmoves:
                        if self.validcell(i+di, j+dy):
                            if self.emptycell(i+di, j+dy) or self.opponentspiece(self.board[i+di][j+dy]):
                                p = self.clone()
                                p.movepiece(i, j, i+di, j+dy)
                                ret.append(p)

        return ret

    def bishopmoves(self):
        ret = []

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == self.bishopsymbol():
                    directions = [
                        (1,   1),
                        (1,  -1),
                        (-1,  1),
                        (-1, -1),
                    ]
                    for di, dy in directions:
                        for k in range(1, 8):
                            if self.validcell(i+(k*di), j+(k*dy)):
                                if self.emptycell(i+(k*di), j+(k*dy)):
                                    p = self.clone()
                                    p.movepiece(i, j, i+(k*di), j+(k*dy))
                                    ret.append(p)
                                    continue
                                if self.opponentspiece(self.board[i+(k*di)][j+(k*dy)]):
                                    p = self.clone()
                                    p.movepiece(i, j, i+(k*di), j+(k*dy))
                                    ret.append(p)
                                break

        return ret

    def rookmoves(self):
        ret = []

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == self.rooksymbol():
                    directions = [
                        (1,  0),
                        (-1, 0),
                        (0,  1),
                        (0, -1),
                    ]
                    for di, dy in directions:
                        for k in range(1, 8):
                            if self.validcell(i+(k*di), j+(k*dy)):
                                if self.emptycell(i+(k*di), j+(k*dy)):
                                    p = self.clone()
                                    p.movepiece(i, j, i+(k*di), j+(k*dy))
                                    ret.append(p)
                                    continue
                                if self.opponentspiece(self.board[i+(k*di)][j+(k*dy)]):
                                    p = self.clone()
                                    p.movepiece(i, j, i+(k*di), j+(k*dy))
                                    ret.append(p)
                                break

        return ret

    def queenmoves(self):
        ret = []

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == self.queensymbol():
                    directions = [
                        (1,   1),
                        (1,   0),
                        (1,  -1),
                        (0,   1),
                        (0,  -1),
                        (-1,  1),
                        (-1,  0),
                        (-1, -1),
                    ]
                    for di, dy in directions:
                        for k in range(1, 8):
                            if self.validcell(i+(k*di), j+(k*dy)):
                                if self.emptycell(i+(k*di), j+(k*dy)):
                                    p = self.clone()
                                    p.movepiece(i, j, i+(k*di), j+(k*dy))
                                    ret.append(p)
                                    continue
                                if self.opponentspiece(self.board[i+(k*di)][j+(k*dy)]):
                                    p = self.clone()
                                    p.movepiece(i, j, i+(k*di), j+(k*dy))
                                    ret.append(p)
                                break

        return ret

    def pseudolegalmoves(self):
        moves = []

        moves += self.kingmoves()
        moves += self.knightmoves()
        moves += self.bishopmoves()
        moves += self.rookmoves()
        moves += self.queenmoves()

        for m in moves:
            m.whitesTurn = not m.whitesTurn

        return moves

    def hasking(self):
        kings = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] in "kK":
                    kings += 1
        return kings == 2

    def legalmoves(self):
        for j in range(8):
            if self.board[0][j] in "kK":
                return []

        ret = []
        for p in self.pseudolegalmoves():
            good = True
            good &= all(q.hasking() for q in p.pseudolegalmoves())
            p.whitesTurn = not p.whitesTurn
            good &= all(q.hasking() for q in p.pseudolegalmoves())
            p.whitesTurn = not p.whitesTurn
            if good:
                ret.append(p)
        return ret

    def piecevalue(self, piece):
        scale = 1
        D = {
            "k": 0*scale,
            "q": 7*scale,
            "r": 5*scale,
            "b": 4*scale,
            "n": 1*scale,
        }

        return D[piece.lower()]

    def evaluate(self):
        score = 0

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == "K":
                    if i == 0:
                        score += inf
                    else:
                        score += (8-i)**1.9
                if self.board[i][j] == "k":
                    if i == 0:
                        score -= inf
                    else:
                        score -= (8-i)**1.9
                if self.board[i][j].isupper():
                    score += self.piecevalue(self.board[i][j])
                if self.board[i][j].islower():
                    score -= self.piecevalue(self.board[i][j])

        return score if self.whitesTurn else -score

    def __lt__(self, other):
        return self.evaluate() < other.evaluate()

if __name__ == '__main__':
    from sys import stdin

    if not stdin.isatty():
        p = Position().parse(stdin.read())
        print(p)
