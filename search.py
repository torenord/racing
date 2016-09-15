inf = 1000

def negamax(position, depth, a, b):
    if depth == 0:
        return position.evaluate(), []

    MAX = -inf

    moves = sorted(position.legalmoves())
    bestline = []

    for p in moves:
        score, line = negamax(p, depth-1, -b, -a)
        score = -score

        if score > MAX:
            MAX = score
            a = max(a, score)
            bestline = [p] + line

        if a >= b:
            break

    return MAX, bestline
