import math

def scale(x):
    a = .5
    if x >= 0:
        return (a * math.pow(x, 3) + (1 - a) * x)
    else:
        return (a * math.pow(x, 3) + (1 - a) * x)

print(scale(.5))
