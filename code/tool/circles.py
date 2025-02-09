import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from typing import Union # type: ignore
from point import Point, midPoint
from line import Line, Segment, Ray

class Circle(object):
    """ f = (x - center.x)^2 + (y - center.y)^2 - radius^2 """
    def __init__(self, center: 'Point', radius):
        self.c = center
        self.r = radius
        self.cirVec = np.array([center.x, center.y, radius])

    def inCircle(self, other: 'Point'):
        func = (other.x - self.c.x)**2 + (other.y - self.c.y)**2 - (self.r)**2
        if func > 0:
            return False
        else:
            return True
        
    def __str__(self):
        return f"Circle at ({self.c.x}, {self.c.y}), r = {self.r}"


"""A = Point(1, 1)
B = Point(5, 5)
C = Point(5, 1)
D = Point(8, 8)
E = Point(3, 3)
F = Point(0, 0)

c = Circle(A, Segment(A, E).getlength())


print(c.inCircle(B), c.inCircle(D), c.inCircle(E), c.inCircle(F), c.inCircle(C))"""
