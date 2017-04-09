import math

x = float(input("x: "))
y = float(input("y: "))
degrees = math.atan2(x, y) / math.pi * 180

if degrees < 0:
    degrees += 360

print(degrees)
