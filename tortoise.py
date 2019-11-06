import turtle

from maths import clamp

MOUSE_LEFT = 1
MOUSE_MIDDLE = 2
MOUSE_RIGHT = 3

KEY_UP = "Up"
KEY_DOWN = "Down"
KEY_LEFT = "Left"
KEY_RIGHT = "Right"

screen = turtle.Screen()


def init(size_canvas, size_window):
    _init_canvas(size_canvas, size_window)
    turtle.register_shape("robot", _robot_shape())
    _setup_events(size_canvas)


def _init_canvas(size_canvas, size_window):
    screen.size_canvas = size_canvas
    screen.robots = []

    turtle.setup(size_window, size_window)
    turtle.setworldcoordinates(-size_canvas, -size_canvas, size_canvas, size_canvas)

    turtle.tracer(0, 0)  # only turtle.update


def _robot_shape():
    shape = turtle.Shape("compound")

    WIDTH = 15
    HEIGHT = 20

    def add_box(center, extents, fill="black", outline=None):
        low = (center[0] - extents[0], center[1] - extents[1])
        high = (center[0] + extents[0], center[1] + extents[1])

        poly = (
            (low[0], low[1]),
            (low[0], high[1]),
            (high[0], high[1]),
            (high[0], low[1]),
        )
        shape.addcomponent(poly, fill, outline)

    # body
    # add_box((-WIDTH, -HEIGHT), (WIDTH, HEIGHT), "blue", "black")
    add_box((0, 0), (WIDTH, HEIGHT), "blue", "black")

    # eyes
    SIZE_EYES = 5
    add_box((WIDTH / 2, HEIGHT), (SIZE_EYES, SIZE_EYES), "white", "black")
    add_box((WIDTH / -2, HEIGHT), (SIZE_EYES, SIZE_EYES), "white", "black")
    # pupils
    SIZE_PUPILS = 2
    add_box((WIDTH / 2, HEIGHT + SIZE_EYES - SIZE_PUPILS), (SIZE_PUPILS, SIZE_PUPILS))
    add_box((WIDTH / -2, HEIGHT + SIZE_EYES - SIZE_PUPILS), (SIZE_PUPILS, SIZE_PUPILS))

    # wheels
    SIZE_WHEEL = (3, 6)
    add_box((WIDTH, -1 + HEIGHT / 2), SIZE_WHEEL)
    add_box((WIDTH, -1 + HEIGHT / -2), SIZE_WHEEL)
    add_box((-WIDTH, -1 + HEIGHT / 2), SIZE_WHEEL)
    add_box((-WIDTH, -1 + HEIGHT / -2), SIZE_WHEEL)

    return shape


def _setup_events(size_canvas):
    # Mouse position

    screen.mousepos = (0, 0)

    def onmove(event):
        screen.mousepos = (
            clamp(screen.cv.canvasx(event.x) / screen.xscale / size_canvas),
            clamp(-screen.cv.canvasy(event.y) / screen.yscale / size_canvas),
        )

    screen.cv.bind("<Motion>", onmove, "+")

    # Mouse buttons

    screen.mousedown = {}
    screen.keys = screen.mousedown

    def mouseevent(button, on):
        def handler(event=None):
            screen.keys[button] = on

        return handler

    keypress = mouseevent

    for btn in (MOUSE_LEFT, MOUSE_MIDDLE, MOUSE_RIGHT):
        screen.mousedown[btn] = False

        screen.cv.bind(f"<Button-{btn}>", mouseevent(btn, True), "+")
        screen.cv.bind(f"<Button{btn}-ButtonRelease>", mouseevent(btn, False), "+")

    for btn in (KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT):
        screen.keys[btn] = False

        screen.onkeypress(keypress(btn, True), btn)
        screen.onkeyrelease(keypress(btn, False), btn)

    # Application lifecycle

    def quit():
        print("QUIT")
        screen.bye()

    screen.onkey(quit, "q")

    def clear():
        for r in screen.robots:
            r.t.clear()

    screen.onkey(clear, "c")

    def reset():
        for r in screen.robots:
            r.reset()

    screen.onkey(reset, "r")


def Pen():
    pen = turtle.Pen(shape="robot", undobuffersize=0)
    pen.speed(0)
    pen.radians()  # heading given in radians

    # fix bug in turtle where custom canvas scaling breaks angles
    # turtle.py, Line 1559 should read `if mode in ["standard", "world"]:`
    pen._setmode(pen._setmode())

    return pen


def mainloop(r, timer=lambda: None, delay=10):
    def ontimer():
        timer()
        starttimer()

    def starttimer():
        r.tick()
        turtle.update()
        turtle.ontimer(ontimer, delay)

    r.reset_time()
    starttimer()
    screen.listen()
    turtle.mainloop()
