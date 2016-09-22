inf = 1000

transpositions = {}

def K(x):
    if x in transpositions:
        return transpositions[x]["score"]
    else:
        return x.evaluate()

def negamax(position, depth, a, b):
    if depth == 0:
        return {
            "depth": depth,
            "score": position.evaluate(),
            "line": [],
        }

    if position in transpositions and transpositions[position]["depth"] >= depth:
        return transpositions[position]

    MAX = -inf

    moves = sorted(position.legalmoves(), key=K)

    bestline = []

    for p in moves:
        result = negamax(p, depth-1, -b, -a)
        score = result["score"]
        line = result["line"]
        score = -score

        if score > MAX:
            MAX = score
            a = max(a, score)
            bestline = [p] + line

        if a >= b:
            break

    transpositions[position] = {
        "depth": depth,
        "score": MAX,
        "line": bestline,
    }

    return transpositions[position]
