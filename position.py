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

    whitePieces = "KQRBN"
    blackPieces = "kqrbn"

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

    def emptycell(self, i, j):
        return self.board[i][j] == " "

    def opponentspiece(self, p):
        return p.islower() == self.whitesTurn

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

    def closepiecemoves(self, symbol, moves):
        ret = []

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == symbol:
                    for di, dy in moves:
                        if 0 <= (i+di) and (i+di) < 8 and 0 <= (j+dy) and (j+dy) < 8:
                            if self.board[i+di][j+dy] == " " or self.board[i+di][j+dy].islower() == self.whitesTurn:
                                p = self.clone()
                                p.movepiece(i, j, i+di, j+dy)
                                ret.append(p)

        return ret

    def rangedpiecemoves(self, symbol, directions):
        ret = []

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == symbol:
                    for di, dy in directions:
                        for k in range(1, 8):
                            if 0 <= i+(k*di) and i+(k*di) < 8 and 0 <= j+(k*dy) and j+(k*dy) < 8:
                                if self.board[i+(k*di)][j+(k*dy)] == " ":
                                    p = self.clone()
                                    p.movepiece(i, j, i+(k*di), j+(k*dy))
                                    ret.append(p)
                                    continue
                                if self.board[i+(k*di)][j+(k*dy)].islower() == self.whitesTurn:
                                    p = self.clone()
                                    p.movepiece(i, j, i+(k*di), j+(k*dy))
                                    ret.append(p)
                                break

        return ret

    kingmoves = (
        (1,   1),
        (1,   0),
        (1,  -1),
        (0,   1),
        (0,  -1),
        (-1,  1),
        (-1,  0),
        (-1, -1),
    )

    knightmoves = (
        (2,  -1),
        (2,   1),
        (1,  -2),
        (1,   2),
        (-1, -2),
        (-1,  2),
        (-2, -1),
        (-2,  1),
    )

    bishopmoves = (
        (1,   1),
        (1,  -1),
        (-1,  1),
        (-1, -1),
    )

    rookmoves = (
        (1,  0),
        (-1, 0),
        (0,  1),
        (0, -1),
    )

    queenmoves = (
        (1,   1),
        (1,   0),
        (1,  -1),
        (0,   1),
        (0,  -1),
        (-1,  1),
        (-1,  0),
        (-1, -1),
    )

    def pseudolegalmoves(self):
        moves = []

        # King moves
        moves += self.closepiecemoves("K" if self.whitesTurn else "k", self.kingmoves)

        # Knight moves
        moves += self.closepiecemoves("N" if self.whitesTurn else "n", self.knightmoves)

        # Bishop moves
        moves += self.rangedpiecemoves("B" if self.whitesTurn else "b", self.bishopmoves)

        # Rook moves
        moves += self.rangedpiecemoves("R" if self.whitesTurn else "r", self.rookmoves)

        # Queen moves
        moves += self.rangedpiecemoves("Q" if self.whitesTurn else "q", self.queenmoves)

        for m in moves:
            m.whitesTurn = not m.whitesTurn

        return moves

    def hasking(self):
        kings = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] in "kK":
                    kings += 1
                    if kings == 2:
                        return True
        return False

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

    scale = 1
    piecevalue = {
        "k": 0*scale,
        "q": 7*scale,
        "r": 5*scale,
        "b": 4*scale,
        "n": 1*scale,
        "K": 0*scale,
        "Q": 7*scale,
        "R": 5*scale,
        "B": 4*scale,
        "N": 1*scale,
    }

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
                if self.board[i][j] in self.whitePieces:
                    score += self.piecevalue[self.board[i][j]]
                if self.board[i][j] in self.blackPieces:
                    score -= self.piecevalue[self.board[i][j]]

        return score if self.whitesTurn else -score

    def __lt__(self, other):
        return self.evaluate() < other.evaluate()

    def __eq__(self, other):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != other.board[i][j]:
                    return False
        if self.whitesTurn != other.whitesTurn:
            return False
        return True

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board)) ^ hash(self.whitesTurn)

if __name__ == '__main__':
    from sys import stdin

    if not stdin.isatty():
        p = Position().parse(stdin.read())
        print(p)
