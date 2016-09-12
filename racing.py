from math import inf

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

COLORS = True

class Board:
    def parse(s):
        board = []

        for row in s.strip().split("\n")[1:-1]:
            board.append([row[2:-2][i] for i in range(0, 16, 2)])

        ret = Board()
        ret.board = board

        return ret

    def copy(self):
        b = Board()
        b.board = []
        for row in self.board:
            b.board.append(row[:])
        return b

    def validcell(self, i, j):
        return 0 <= i and i < 8 and 0 <= j and j < 8

    def emptycell(self, i, j):
        return self.board[i][j] == " "

    def movepiece(self, x1, y1, x2, y2):
        self.board[x2][y2] = self.board[x1][y1]
        self.board[x1][y1] = " "

class Position:
    whitesTurn = True

    def __init__(self, board, whitesTurn):
        self.board = board
        self.whitesTurn = whitesTurn

    def __repr__(self):
        ret = "   +---+---+---+---+---+---+---+---+\n"

        for i in range(8):
            ret += " " + str(8-i) + " | " + " | ".join(self.board.board[i]) + " |\n"

            if COLORS:
                for blackpiece in "kqrbn":
                    ret = ret.replace(blackpiece, bcolors.BOLD + bcolors.FAIL + blackpiece + bcolors.ENDC)

            ret += "   +---+---+---+---+---+---+---+---+\n"

        if self.whitesTurn:
            ret += "     a   b   c   d   e   f   g   h   " + "\u2588"
        else:
            if COLORS:
                ret += " " + bcolors.FAIL + "\u2588" + bcolors.ENDC + "   a   b   c   d   e   f   g   h"
            else:
                ret += " " + "\u2588" +  "   a   b   c   d   e   f   g   h"

        return ret

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

    def flipcolor(self, piece):
        return piece.lower() if piece.isupper() else piece.upper()

    def hasking(self):
        kings = 0
        for i in range(8):
            for j in range(8):
                if self.board.board[i][j] in "kK":
                    kings += 1
        return kings == 2

    def opponentskingincheck(self):
        return any(not p.board.hasking() for p in self.legalmoves())

    def legalkingmoves(self):
        ret = []

        for i in range(8):
            for j in range(8):
                if self.board.board[i][j] == self.kingsymbol():
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
                        if self.board.validcell(i+di, j+dy) and (self.board.emptycell(i+di, j+dy) or self.opponentspiece(self.board.board[i+di][j+dy])):
                            b = self.board.copy()
                            b.movepiece(i, j, i+di, j+dy)
                            ret.append(Position(b, self.whitesTurn))

        return ret

    def legalknightmoves(self):
        ret = []

        for i in range(8):
            for j in range(8):
                if self.board.board[i][j] == self.knightsymbol():
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
                        if self.board.validcell(i+di, j+dy) and (self.board.emptycell(i+di, j+dy) or self.opponentspiece(self.board.board[i+di][j+dy])):
                            b = self.board.copy()
                            b.movepiece(i, j, i+di, j+dy)
                            ret.append(Position(b, self.whitesTurn))

        return ret

    def legalbishopmoves(self):
        ret = []

        for i in range(8):
            for j in range(8):
                if self.board.board[i][j] == self.bishopsymbol():
                    directions = [
                        (1,   1),
                        (1,  -1),
                        (-1,  1),
                        (-1, -1),
                    ]
                    for di, dy in directions:
                        for k in range(1, 8):
                            if self.board.validcell(i+(k*di), j+(k*dy)):
                                if self.board.emptycell(i+(k*di), j+(k*dy)):
                                    b = self.board.copy()
                                    b.movepiece(i, j, i+(k*di), j+(k*dy))
                                    ret.append(Position(b, self.whitesTurn))
                                    continue
                                if self.opponentspiece(self.board.board[i+(k*di)][j+(k*dy)]):
                                    b = self.board.copy()
                                    b.movepiece(i, j, i+(k*di), j+(k*dy))
                                    ret.append(Position(b, self.whitesTurn))
                                break

        return ret

    def legalrookmoves(self):
        ret = []

        for i in range(8):
            for j in range(8):
                if self.board.board[i][j] == self.rooksymbol():
                    directions = [
                        (1,  0),
                        (-1, 0),
                        (0,  1),
                        (0, -1),
                    ]
                    for di, dy in directions:
                        for k in range(1, 8):
                            if self.board.validcell(i+(k*di), j+(k*dy)):
                                if self.board.emptycell(i+(k*di), j+(k*dy)):
                                    b = self.board.copy()
                                    b.movepiece(i, j, i+(k*di), j+(k*dy))
                                    ret.append(Position(b, self.whitesTurn))
                                    continue
                                if self.opponentspiece(self.board.board[i+(k*di)][j+(k*dy)]):
                                    b = self.board.copy()
                                    b.movepiece(i, j, i+(k*di), j+(k*dy))
                                    ret.append(Position(b, self.whitesTurn))
                                break

        return ret

    def legalqueenmoves(self):
        ret = []

        for i in range(8):
            for j in range(8):
                if self.board.board[i][j] == self.queensymbol():
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
                            if self.board.validcell(i+(k*di), j+(k*dy)):
                                if self.board.emptycell(i+(k*di), j+(k*dy)):
                                    b = self.board.copy()
                                    b.movepiece(i, j, i+(k*di), j+(k*dy))
                                    ret.append(Position(b, self.whitesTurn))
                                    continue
                                if self.opponentspiece(self.board.board[i+(k*di)][j+(k*dy)]):
                                    b = self.board.copy()
                                    b.movepiece(i, j, i+(k*di), j+(k*dy))
                                    ret.append(Position(b, self.whitesTurn))
                                break

        return ret

    def legalmoves(self):
        moves = []

        moves += self.legalkingmoves()
        moves += self.legalknightmoves()
        moves += self.legalbishopmoves()
        moves += self.legalrookmoves()
        moves += self.legalqueenmoves()

        for m in moves:
            m.whitesTurn = not m.whitesTurn

        return moves

    def reallylegal(self):
        for j in range(8):
            if self.board.board[0][j] in "kK":
                return []

        ret = []
        for p in self.legalmoves():
            good = True
            good &= all(q.hasking() for q in p.legalmoves())
            p.whitesTurn = not p.whitesTurn
            good &= all(q.hasking() for q in p.legalmoves())
            p.whitesTurn = not p.whitesTurn
            if good:
                ret.append(p)
        return ret

    def evaluate(self):
        score = 0

        for i in range(8):
            for j in range(8):
                if self.board.board[i][j] == "K":
                    if i == 0:
                        score = inf
                    else:
                        score += 8-i
                if self.board.board[i][j] == "k":
                    if i == 0:
                        score = -inf
                    else:
                        score -= 8-i

        return score if self.whitesTurn else -score

    def negamax(self, depth):
        if depth == 0:
            return self.evaluate()

        MAX = -inf

        for p in self.reallylegal():
            score = -p.negamax(depth-1)

            if score > MAX:
                MAX = score

        return MAX

    def negamaxab(self, depth, a, b):
        if depth == 0:
            return self.evaluate()

        MAX = -inf

        moves = self.reallylegal()
        moves = sorted(moves, reverse=True)

        for p in moves:
            score = -p.negamaxab(depth-1, -b, -a)

            MAX = max(MAX, score)
            a = max(a, score)

            if a >= b:
                break

        return MAX

    def __lt__(self, other):
        return self.evaluate() < other.evaluate()

import sys

if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    filename = "test.txt"

P = Position(Board.parse(open(filename).read()), True)

def decode(s):
    x = ord(s[0]) - ord("a")
    y = 8 - int(s[1])

    return x, y

import readline

defaultdepth = 1

while True:
    try:
        inp = input("> ")
    except EOFError:
        print()
        break
    if inp == "q":
        break
    elif inp == "p":
        print(P)
    elif inp.split(" ")[0] == "l":
        filename = inp.split(" ")[1]
        P = Position(Board.parse(open(filename).read()), True)
    elif inp.split(" ")[0] == "m":
        a = inp.split(" ")[1]
        b = inp.split(" ")[2]

        y1, x1 = decode(a)
        y2, x2 = decode(b)

        P.board.movepiece(x1, y1, x2, y2)
        P.whitesTurn = not P.whitesTurn
        print(P)
    elif inp.split(" ")[0] == "e":
        try:
            depth = int(inp.split(" ")[1])
        except:
            depth = defaultdepth
        print(-P.negamax(depth))
    elif inp.split(" ")[0] == "c":
        try:
            depth = int(inp.split(" ")[1])
        except:
            depth = defaultdepth
        maxscore = -inf
        best = None
        for p in P.reallylegal():
            score = -p.negamax(depth)
            if score >= maxscore:
                maxscore = score
                best = p
        if best:
            P = best
            print(P)
    elif inp.split(" ")[0] == "a":
        try:
            depth = int(inp.split(" ")[1])
        except:
            depth = defaultdepth
        maxscore = -inf
        best = None
        for p in P.reallylegal():
            score = -p.negamaxab(depth, -inf, inf)
            if score >= maxscore:
                maxscore = score
                best = p
        if best:
            P = best
            print(P)
    elif inp.split(" ")[0] == "n":
        try:
            depth = int(inp.split(" ")[1])
        except:
            depth = defaultdepth
        for p in P.reallylegal():
            print(p)
            print(-p.negamax(depth))
    elif inp.split(" ")[0] == "x":
        print(P.negamax(int(inp.split(" ")[1])))
