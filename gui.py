from position import Position
from search import negamax
inf = 1000

p = Position().setup()

import pyglet

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

square_size = 75

window = pyglet.window.Window(8*square_size, 8*square_size)

cursor = window.get_system_mouse_cursor(window.CURSOR_HAND)
window.set_mouse_cursor(cursor)

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

selected_square = None

@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    # global selected_square
    # selected_square = int((x+dx) / square_size), int((y+dy) / square_size)
    # window.invalid = True
    global selected_square
    selected_square = int(x / square_size), int(y / square_size)
    window.invalid = True

@window.event
def on_mouse_press(x, y, button, modifiers):
    global selected_square
    i, j = int(x / square_size), int(y / square_size)
    if selected_square:
        if (i, j) == selected_square:
            selected_square = None
        else:
            p.movepiece(7-selected_square[1], selected_square[0], 7-j, i)
            p.whitesTurn = not p.whitesTurn
            selected_square = None
    else:
        selected_square = (i, j)
    window.invalid = True

@window.event
def on_draw():
    window.clear()
    for i in range(8):
        for j in range(8):
            color = (255, 255, 255, 255) if (i+j) % 2 == 1 else (128, 160, 192, 255)
            draw_rect(square_size*i, square_size*j, square_size, square_size, color)
    if selected_square:
        color = (192, 224, 255, 255)
        draw_rect(square_size*selected_square[0], square_size*selected_square[1], square_size, square_size, color)
    for piece in render_pieces():
        piece.draw()

def update(dt):
    window.invalid = True

pyglet.clock.schedule_interval(update, 0.5)

import threading

def worker(pos):
    from cli import do
    do(pos)

t = threading.Thread(target=worker, args=(p,))
t.daemon = True
t.start()

pyglet.app.run()

t.join()
