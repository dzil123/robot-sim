import turtle


MOUSE_LEFT = 1
MOUSE_MIDDLE = 2
MOUSE_RIGHT = 3


screen = turtle.Screen()


def init(size_canvas=5, size_window=500):
    _init_canvas(size_canvas, size_window)
    turtle.register_shape("robot", _robot_shape())


def _init_canvas(size_canvas, size_window):
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


def _setup_events():
    screen.mousepos = (0, 0)
    screen.mousedown = {}

    def onmove(event):
        screen.mousepos = (
            screen.cv.canvasx(event.x) / screen.xscale,
            -screen.cv.canvasy(event.y) / screen.yscale,
        )

    screen.cv.bind("<Motion>", onmove, "+")

    def mouseevent(button, on):
        def handler(event):
            screen.mousedown[button] = on

        return handler

    for button in (MOUSE_LEFT, MOUSE_MIDDLE, MOUSE_RIGHT):
        screen.mousedown[button] = False

        screen.cv.bind(f"<Button-{button}>", mouseevent(button, True), "+")
        screen.cv.bind(
            f"<Button{button}-ButtonRelease>", mouseevent(button, False), "+"
        )


def Pen():
    pen = turtle.Pen(shape="robot", undobuffersize=0)
    pen.speed(0)
    pen.radians()  # heading given in radians

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
    turtle.mainloop()
