# -*- coding: utf-8 -*-
import math

def polar(x, y):
    """returns r, theta(degrees)"""
    r = (x ** 2 + y ** 2) ** .5
    theta = (int(math.degrees(math.atan2((-1)*y, x))) + 450) % 360
    return r, theta

def rec(r, theta):
    """returns x, x"""
    x = float("{0:.8f}".format(r * math.cos(math.radians(((theta) % 360) + 270)))) + 0
    y = float("{0:.8f}".format(r * math.sin(math.radians(((theta) % 360) + 270)))) * (-1) + 0
    return (x, y)

print("\npolar(x=1.0, y=0.0) y rec(r=1.0, a=90)")
print("r, a", polar(1.0, 0.0))
print("x, y", rec(1.0, 90))

print("\npolar(x=1.0, y=1.0) y rec(r=1.4142135623730951, a=45)")
print("r, a", polar(1.0, 1.0))
print("x, y", rec(1.4142135623730951, 45))

print("\npolar(x=0.0, y=1.0) y rec(r=1.0, a=0)")
print("r, a", polar(0.0, 1.0))
print("x, y", rec(1.0, 0))

print("\npolar(x=-1.0, y=1.0) y rec(r=1.4142135623730951, a=315)")
print("r, a", polar(-1.0, 1.0))
print("x, y", rec(1.4142135623730951, 315))

print("\npolar(x=-1.0, y=0.0) y rec(r=1.0, a=270)")
print("r, a", polar(-1.0, 0.0))
print("x, y", rec(1.0, 270))

print("\npolar(x=-1.0, y=-1.0) y rec(r=1.4142135623730951, a=225)")
print("r, a", polar(-1.0, -1.0))
print("x, y", rec(1.4142135623730951, 225))

print("\npolar(x=0.0, y=-1.0) y rec(r=1.0, a=180)")
print("r, a", polar(0.0, -1.0))
print("x, y", rec(1.0, 180))

print("\npolar(x=1.0, y=-1.0) y rec(r=1.4142135623730951, a=135)")
print("r, a", polar(1.0, -1.0))
print("x, y", rec(1.4142135623730951, 135))

print("\npolar(x=0.0, y=0.0) y rec(r=0.0, a=90)")
print("r, a", polar(0.0, 0.0))
print("x, y", rec(0.0, 90))

#corregir si el resultado es -0
#print(-0+0)
#
print("x, y", rec(12, 55))