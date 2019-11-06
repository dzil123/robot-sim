import numpy as np

np.set_printoptions(precision=4, suppress=True, sign=" ")

copysign = np.copysign


def Vector():
    return np.zeros(shape=(2))


def lerp(x, a, b):
    return np.interp(x, (0, 1), (a, b))


def anyClamp(x, low, high):
    return np.max((low, np.min((high, x))))


def clamp(x):
    return anyClamp(x, -1, 1)


def clamp01(x):
    return anyClamp(x, 0, 1)


def deadband(*, minOut=0, deadband=0, maxIn=1, maxOut=1, square=False):
    minOut = clamp01(abs(minOut))
    deadband = clamp01(abs(deadband))
    maxIn = clamp01(abs(maxIn))
    maxOut = clamp01(abs(maxOut))
    square = bool(square)

    m = (1 - minOut) / (maxIn - deadband)

    def calc(input):
        input = anyClamp(input, -maxIn, maxIn)

        if abs(input) <= deadband:
            output = 0
        elif input > 0:
            output = m * (input - deadband) + minOut
        else:
            output = m * (input + deadband) - minOut

        output = clamp(output)

        if square:
            output = copysign(output * output, output)

        return output

    return calc
