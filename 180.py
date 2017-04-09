import math

while True:
    x = float(input("x: "))
    y = float(input("y: "))
    deg = math.atan2(x, y) / math.pi * 180

    if deg < 0:
        deg = deg + 360

    print(math.floor(deg))
