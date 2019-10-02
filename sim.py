import turtle
import time
import numpy as np

MOUSE_LEFT = 1
MOUSE_MIDDLE = 2
MOUSE_RIGHT = 3


def init_turtle():
    # Setup canvas

    SIZE_CANVAS = 5
    SIZE_WINDOW = 500

    turtle.setup(SIZE_WINDOW, SIZE_WINDOW)
    turtle.setworldcoordinates(-SIZE_CANVAS, -SIZE_CANVAS, SIZE_CANVAS, SIZE_CANVAS)

    turtle.tracer(0, 0)  # only turtle.update

    # Create robot shape

    robot_shape = turtle.Shape("compound")

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
        robot_shape.addcomponent(poly, fill, outline)

    # body
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

    turtle.register_shape("robot", robot_shape)

    # Setup events

    screen = turtle.Screen()  # singleton
    screen.mousepos = (0, 0)
    screen.mousedown = {}

    def onmove(event):
        screen.mousepos = (
            screen.cv.canvasx(event.x) / screen.xscale,
            -screen.cv.canvasy(event.y) / screen.yscale,
        )

    screen.cv.bind("<Motion>", onmove, '+')

    def mouseevent(button, on):
        def handler(event):
            screen.mousedown[button] = on

        return handler
    
    for button in (MOUSE_LEFT, MOUSE_MIDDLE, MOUSE_RIGHT):
        screen.mousedown[button] = False

        screen.cv.bind(f"<Button-{button}>", mouseevent(button, True), '+')
        screen.cv.bind(f"<Button{button}-ButtonRelease>", mouseevent(button, False), '+')


def make_pen():
    pen = turtle.Pen(shape="robot", undobuffersize=0)
    pen.speed(0)

    return pen

def Vector():
    return np.zeros(shape=(2))

class Robot:
    def __init__(self):
        self.t = make_pen()

        self.p = Vector()
        self.v = Vector()
        self.a = Vector()

        self.last_time = time.time()

    def _tick(self, dt):
        pass

    def tick(self):
        t = time.time()
        dt = t - self.last_time
        self.last_time = t

        MAX_DT = 0.05

        while dt > MAX_DT:
            self._tick(MAX_DT)
            dt -= MAX_DT
        
        if dt < 0:
            return
        
        self._tick(dt)

    def drive(self, l, r):
        self.a[0] = l
        self.a[1] = r
    
    def drive_straight(self, v):
        self.drive(v, v)


init_turtle()
r = Robot()

def mainloop(timer=lambda: None, delay=10):
    def ontimer():
        timer()
        starttimer()

    def starttimer():
        turtle.update()
        turtle.ontimer(ontimer, delay)

    starttimer()
    turtle.mainloop()

def lerp(x, a, b):
    return (1 - x) * a + x * b

def main():
    screen = turtle.Screen()
    r.t.goto(-5, -5)
    r.t.clear()

    def timer():
        sec = time.time() - r.last_time
        r.last_time = 
        # sec /= 10
        sec -= 5
        # sec = min(sec, 1)


        r.t.goto(lerp(0.01, r.t.xcor(), 4), sec)
        print(r.t.xcor())

        # print("Pos:", screen.mousepos)
        # print("Click:", screen.mousedown)

    mainloop(timer)


if __name__ == "__main__":
    main()
