from position import Position
from search import negamax
inf = 1000

p = Position().setup()

import pyglet

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

square_size = 75

window = pyglet.window.Window(8*square_size, 8*square_size)

D = {
    "K": pyglet.resource.image("white_king.png"),
    "Q": pyglet.resource.image("white_queen.png"),
    "R": pyglet.resource.image("white_rook.png"),
    "B": pyglet.resource.image("white_bishop.png"),
    "N": pyglet.resource.image("white_knight.png"),
    "P": pyglet.resource.image("white_pawn.png"),
    "k": pyglet.resource.image("black_king.png"),
    "q": pyglet.resource.image("black_queen.png"),
    "r": pyglet.resource.image("black_rook.png"),
    "b": pyglet.resource.image("black_bishop.png"),
    "n": pyglet.resource.image("black_knight.png"),
    "p": pyglet.resource.image("black_pawn.png"),
}

def draw_rect(x, y, width, height, color):
    width = int(round(width))
    height = int(round(height))
    image_pattern = pyglet.image.SolidColorImagePattern(color=color)
    image = image_pattern.create_image(width, height)
    image.blit(x, y)

def render_pieces():
    pieces = []

    for i in range(8):
        for j in range(8):
            if p.board[i][j] != " ":
                image = D[p.board[i][j]]
                image.width = square_size
                image.height = square_size
                piece = pyglet.sprite.Sprite(img=image, x=square_size*j, y=square_size*(7-i))
                pieces.append(piece)

    return pieces

@window.event
def on_draw():
    window.clear()
    for i in range(8):
        for j in range(8):
            color = (255, 255, 255, 255) if (i+j) % 2 == 0 else (128, 128, 128, 255)
            draw_rect(square_size*i, square_size*j, square_size, square_size, color)
    for piece in render_pieces():
        piece.draw()

def update(dt):
    global p
    score, line = negamax(p, 2, -inf, inf)
    p = line[0]

pyglet.clock.schedule_interval(update, 0.5)

pyglet.app.run()
