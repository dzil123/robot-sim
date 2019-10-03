import numpy as np


def Vector():
    return np.zeros(shape=(2))


def lerp(x, a, b):
    return np.interp(x, (0, 1), (a, b))


def clamp(x):
    return np.max((-1, np.min((1, x))))
