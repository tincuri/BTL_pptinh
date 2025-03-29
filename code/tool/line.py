import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
import sys
from typing import Union
from .point import Point
import math

class Line(object):
    """Represents a line in the form ax + by + c = 0.

    Supports initialization via two points or a coefficient vector.

    Attributes:
        lineVec (numpy.ndarray): Coefficients [a, b, c] of the line equation.

    Methods:
        __init__(*args): Initializes a line from two points or a coefficient vector.
        distance(other: 'Point') -> float: Computes the perpendicular distance to a point.
        isRight(other: 'Point') -> bool: Checks if a point is on the "right" side of the line.
        __str__() -> str: Returns a string representation of the line.
    """
    def __init__(self, *args):
        if len(args) == 2:
            self.p, self.q = args
            self.px, self.py = self.p.coor()
            self.qx, self.qy = self.q.coor()
            self.getfunc()
            self.create = "two points"
        elif len(args) == 1:
            self.lineVec = np.array(*args)
            self.create = "vector"
        else:
            raise ValueError("Invalid arguments. Provide either two points or vector.")

    def getfunc(self):
        if self.py == self.qy:
            a = 0
            b = 1
            c = -self.py
        elif self.px == self.qx:
            a = 1
            b = 0
            c = -self.px
        else:
            a = 1
            #print(self.px, type(self.px)) # debug
            b = - (self.px - self.qx) / (self.py - self.qy)
            c = - self.px - b * self.py
        self.lineVec = np.array([a, b, c])
    
    def distance(self, other: 'Point') -> Union[int, float]:
        vector = np.array([other.coor()[0], other.coor()[1] , 1])
        dist = np.abs( np.dot(vector, self.lineVec) ) / np.sqrt( self.lineVec[0]**2 + self.lineVec[1]**2)
        return dist
    
    def isRight(self, other: 'Point'):
        vector = np.array([other.coor()[0], other.coor()[1] , 1])
        que = np.dot(vector, self.lineVec)
        #dist = np.abs( np.dot(vector, self.lineVec) ) / np.sqrt( self.lineVec[0]**2 + self.lineVec[1]**2)
        return que > 0

    def __str__(self):
        return f"Make from {self.create}."


class Segment(Line):
    """Represents a line segment defined by two points.

    Inherits from Line.

    Methods:
        getlength() -> float: Returns the segment's length.
        distance1(pnt: 'Point') -> float: Computes the shortest distance from the segment to a point.
        onSegment(other: 'Point') -> bool: Checks if a point lies on the segment.
        intersect(other: 'Segment') -> bool: Determines if two segments intersect.
    """
    def getlength(self):
        return self.p.distance(self.q)
    
    def distance1(self, pnt: 'Point'): # distance to the nearest point (start or end) of segment to the Point
        def dot(v, w):
            x, y = v
            X, Y = w
            return x*X + y*Y

        line_vec = (self.qx-self.px, self.qy-self.py)
        pnt_vec = (pnt.x - self.px, pnt.y - self.py)

        line_len = self.getlength()

        line_unitvec = (line_vec[0]/line_len, line_vec[1]/line_len)
        pnt_vec_scaled = (pnt_vec[0]/line_len, pnt_vec[1]/line_len)

        t = dot(line_unitvec, pnt_vec_scaled)
        t = max(0.0, min(1.0, t)) # More concise way to clamp t

        nearest = (line_vec[0] * t, line_vec[1] * t)
        dist = np.sqrt((nearest[0] - pnt_vec[0])**2 + (nearest[1] - pnt_vec[1])**2)
        return dist

    def onSegment(self, other: 'Point'):
        if super().distance(other) != 0:
            return False
        
        x, y = other.coor()
        return min(self.px, self.qx) <= x <= max(self.px, self.qx) and min(self.py, self.qy) <= y <= max(self.py, self.qy)
    
    # ccw use in intersect method
    def ccw_x(self, a, b, c):
        return (c[1]-a[1]) * (b[0]-a[0]) > (b[1]-a[1]) * (c[0]-a[0])


    # Return true if line segments AB and CD intersect
    def intersect(self, other: 'Segment'):
        a = [self.px, self.py]
        b = [self.qx, self.qy]
        c = [other.px, other.py]
        d = [other.qx, other.qy]

        if a == c or a ==d:
            return False
        elif b == c or b == d:
            return False
        
        return self.ccw_x(a, c, d) != self.ccw_x(b, c, d) and self.ccw_x(a, b, c) != self.ccw_x(a, b, d)


class Ray(Line):
    """Represents a Ray in the form ax + by + c = 0.

    Inherited from Line

    Methods:
        onRay(self, other: 'Point'): check if Point is on Ray or not
        restricted(current no thing): restricted to plot
    """
    def onRay(self, other: 'Point'):
        if super().distance(other) != 0:
            return False
        
        x, y = other.coor()
        if not (min(x, self.qx) <= self.px <= max(x, self.qx) and min(y, self.qy) <= self.py <= max(y, self.qy)):
            return True
        return False


"""A = Point(1, 1)
B = Point(2, 2)
C = Point(4, 2)
d = Line(A, B)
c = d.distance(C)
print(c, d.getfunc())"""

"""A = Point(1, 1)
B = Point(5, 5)
C = Point(5, 1)
D = Point(8, 8)
E = Point(3, 3)
F = Point(0, 0)
d = Line(A, B)
d.lineVec
print(d, d.lineVec, d.distance(C))
#print(d.getfunc())
#print(d.onRay(C), d.onRay(D), d.onRay(E), d.onRay(F))

f = Line([1, -1, 0])
print(f, f.lineVec, f.distance(C))
"""

"""A = Point(0, 0)
B = Point(4.456456, 0.5959)
C = Point(7, 2)
ab = Segment(A, B)
h = ab.pnt2line(C)
print(h)"""