#!/usr/bin/env python3
import math

def zero(x):
    if math.fabs(x) <= 0.001:
        return 0
    else:
        return x

def newgyro(vec):
    x1 = vec[0]
    y1 = vec[1]
    angle = vec[2]
    if (angle <= 45 and angle >=0) or (angle <= 359 and angle > 314):
        X1 = x1
        Y1 = y1
    elif angle > 45 and angle <= 135:
        Y1 = -x1
        X1 = y1
    elif angle > 135 and angle <= 225:
        X1 = -x1
        Y1 = -y1
    elif angle > 225 and angle <= 314:
        Y1 = x1
        X1 = -y1 
    return [X1, Y1]

def regular(vec):
    x1 = vec[0]
    y1 = vec[1]
    angle = vec[2]
    x1 = -x1
    y1 = -y1
    if (angle <= 45 and angle >=0) or (angle <= 359 and angle > 314):
        X1 = -x1
        Y1 = -y1
    elif angle > 45 and angle <= 135:
        Y1 = x1
        X1 = -y1
    elif angle > 135 and angle <= 225:
        X1 = x1
        Y1 = y1
    elif angle > 225 and angle <= 314:
        Y1 = -x1
        X1 = y1
    return [X1, Y1]

def linear(vec):
    x1 = vec[0]
    y1 = vec[1]
    angle = vec[2] / 180 * math.pi
    cos = zero(math.cos(angle))
    sin = zero(math.sin(angle))
    rightprime = x1 * cos - y1 * sin
    forwardprime = x1 * sin + y1 * cos
    return [rightprime, forwardprime]

def linear2(vec):
    x1 = vec[0]
    y1 = vec[1]
    angle = vec[2] / 180 * math.pi
    cos = zero(math.cos(angle))
    sin = zero(math.sin(angle))
    rightprime = x1 * cos + y1 * sin
    forwardprime = -x1 * sin + y1 * cos
    return [rightprime, forwardprime]

anglel = int(input("angle: "))
forward = float(input("forward: "))
right = float(input("right: "))
vec = [right, forward, anglel]

reg = regular(vec)
new = newgyro(vec)
lin = linear(vec)
lin2 = linear2(vec)

if reg != new:
    print("we not all good")

if reg == lin:
    print("we good 2")
else:
    print("we not good")
    print("newgyro x: " + repr(new[0] + 0))
    print("newgyro y: " + repr(new[1] + 0))
    print("linear x: " + repr(lin[0] + 0))
    print("linear y: " + repr(lin[1] + 0))
    
if reg != lin2:
    print("linear2 x: " + repr(lin2[0] + 0))
    print("linear2 y: " + repr(lin2[1] + 0))
else:
    print("we also good")

