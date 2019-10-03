import time

from maths import Vector, clamp, lerp, np
from tortoise import Pen, init, mainloop, screen


class Robot:
    def __init__(self):
        self.t = Pen()

        self.width = 1.5

        self.r = 0  # radians
        self.p = Vector()  # position
        self.v = Vector()  # velocity
        self.a = Vector()  # acceleration

        self.reset_time()

    def reset_time(self):
        self.start_time = time.time()
        self.last_time = self.start_time

    @property
    def time(self):
        return time.time() - self.start_time

    def _update_v(self, dt):
        SPEED = 20  # higher = velocity changes faster
        dt *= SPEED

        self.v[0] = lerp(dt, self.v[0], self.a[0])
        self.v[1] = lerp(dt, self.v[1], self.a[1])

        if np.allclose(self.v[0], self.a[0]):
            self.v[0] = self.a[0]

        if np.allclose(self.v[1], self.a[1]):
            self.v[1] = self.a[1]

    def _update_p(self, dt):
        # https://robotics.stackexchange.com/a/1679

        SPEED = 5  # higher = high max velocity
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


init()
r = Robot()


def main():
    r.goto(-5, -5)
    r.t.clear()

    def timer():
        r.drive(*screen.mousepos)
        print(r.p, r.v, r.a)

    mainloop(r, timer)


if __name__ == "__main__":
    main()
