import numpy as np


def Vector():
    return np.zeros(shape=(2))


def lerp(x, a, b):
    return np.interp(x, (0, 1), (a, b))
