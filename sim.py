import math
import time

from maths import Vector, clamp, lerp, np
from tortoise import KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP, Pen, init, mainloop, screen


class Robot:
    def __init__(self):
        screen.robots.append(self)
        self.t = Pen()

        self.width = 1.5  # for simulation, distance between wheels

        self.reset()

    def reset(self):
        self.r = 0  # rotation in radians
        self.p = Vector()  # position
        self.v = Vector()  # velocity
        self.a = Vector()  # acceleration

        self.reset_time()

        self.t.up()
        self._update_t()
        self.t.down()

        self.t.clear()

    def reset_time(self):
        self.start_time = time.time()
        self.last_time = self.start_time

    @property
    def time(self):
        return time.time() - self.start_time

    @property
    def verror(self):
        return np.abs(self.a - self.v)

    def _update_v(self, dt):
        SPEED = 10  # higher = higher acceleration
        dt = clamp(dt * SPEED)

        self.v[0] = lerp(dt, self.v[0], self.a[0])
        self.v[1] = lerp(dt, self.v[1], self.a[1])

        if np.allclose(self.v[0], self.a[0]):
            self.v[0] = self.a[0]

        if np.allclose(self.v[1], self.a[1]):
            self.v[1] = self.a[1]

    def _update_p(self, dt):
        # https://robotics.stackexchange.com/a/1679

        SPEED = 5  # higher = higher velocity
        l, r = dt * self.v * SPEED

        if np.allclose(l, r):
            self.p[0] += l * np.cos(self.r)
            self.p[1] += r * np.sin(self.r)
        else:
            R = self.width * (l + r) / (2 * (r - l))
            wd = (r - l) / self.width

            self.p[0] += R * (np.sin(wd + self.r) - np.sin(self.r))
            self.p[1] -= R * (np.cos(wd + self.r) - np.cos(self.r))
            self.r += wd

    def _update_t(self):
        self.t.goto(*self.p)
        self.t.seth(self.r)

        self._wraparound()

    def _wraparound(self):
        wrap_size = screen.size_canvas * 1.15
        changed = False

        while self.p[0] > wrap_size:
            self.p[0] -= 2 * wrap_size
            changed = True

        while self.p[0] < -wrap_size:
            self.p[0] += 2 * wrap_size
            changed = True

        while self.p[1] > wrap_size:
            self.p[1] -= 2 * wrap_size
            changed = True

        while self.p[1] < -wrap_size:
            self.p[1] += 2 * wrap_size
            changed = True

        if changed:
            self.t.up()
            self.t.goto(*self.p)
            self.t.down()

    def _tick(self, dt):
        self._update_v(dt)
        self._update_p(dt)
        self._update_t()

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

    # everything below this line is the "public interface"

    def goto(self, *pos):
        self.t.goto(*pos)
        self._update_t()

    def drive(self, l, r):
        self.a[0] = clamp(l)
        self.a[1] = clamp(r)

    def drive_straight(self, v):
        self.drive(v, v)

    def drive_arcade(self, throttle, turn):
        epsilon = 0.0001

        max_input = math.copysign(max(abs(throttle), abs(turn)), (throttle + epsilon))

        if (throttle + epsilon) * turn >= 0:
            self.drive(max_input, throttle - turn)
        else:
            self.drive(throttle + turn, max_input)


def drive_screen():
    r.drive(*screen.mousepos)


def drive_screen_arcade():
    r.drive_arcade(*(screen.mousepos[::-1]))


def drive_key_arcade():
    turn = 0
    if screen.keys[KEY_LEFT]:
        turn -= 1
    if screen.keys[KEY_RIGHT]:
        turn += 1

    throttle = 0
    if screen.keys[KEY_UP]:
        throttle += 1
    if screen.keys[KEY_DOWN]:
        throttle -= 1

    r.drive_arcade(throttle, turn)


# change size_window if the window doesn't fit on screen
init(size_canvas=10, size_window=1000)
r = Robot()


def main():
    r.goto(-5, -5)
    r.t.clear()

    def timer():
        drive_screen_arcade()
        print(r.p, r.v, r.a)

    mainloop(r, timer)


if __name__ == "__main__":
    main()

# 'q' to quit
# 'r' to reset
# 'c' to clear

# mouse x coordinate is left wheel velocity
# mouse y coordinate is right wheel velocity

# printout: position, velocity, acceleration

# simulates differential drive
# models acceleration

# change canvas size, window size in init() call above

# write your own timer()
