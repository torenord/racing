inf = 1000

def negamax(position, depth, a, b):
    if depth == 0:
        return position.evaluate()

    MAX = -inf

    moves = sorted(position.legalmoves())

    for p in moves:
        score = -negamax(p, depth-1, -b, -a)

        MAX = max(MAX, score)
        a = max(a, score)

        if a >= b:
            break

    return MAX

def negamaxpos(position, depth, a, b):
    if depth == 0:
        return position

    MAX = -inf
    bestmove = None

    moves = sorted(position.legalmoves())

    for p in moves:
        score = -negamax(p, depth-1, -b, -a)

        if score > MAX:
            bestmove = p
            MAX = score

        a = max(a, score)

        if a >= b:
            break

    return bestmove
