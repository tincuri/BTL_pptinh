import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from typing import Union # type: ignore
from point import Point, midPoint
from line import Line, Segment, Ray

def perpendicular(d: 'Line', p: 'Point') -> 'Line':
    """
    Returns a line perpendicular to the given line `d` that passes through the point `p`.

    Args:
        d (Line): The reference line.
        p (Point): The point through which the perpendicular line will pass.

    Returns:
        Line: A new Line object representing the perpendicular line.

    """
    px, py = p.coor()
    a_line, b_line, c_line = d.lineVec
    def update():
        """
        Return: lineVec
        """
        if a_line == 0:
            a = 1
            b = 0
            c = -px
        elif b_line == 0:
            a = 0
            b = 1
            c = -py
        else:
            a = 1
            b = - a_line / b_line
            c = - a * px - b * py
        lineVec = np.array([a, b, c])
        return lineVec
    return Line(update())

def perp_bisector(seg: 'Segment'):
    """
    Returns the perpendicular bisector of the given line segment `seg`.

    Args:
        seg (Segment): The line segment for which the perpendicular bisector is to be determined.

    Returns:
        Line: A new Line object representing the perpendicular bisector.
    """

    mid = midPoint(seg.p, seg.q)
    seg = Line(seg.p, seg.q)
    return perpendicular(seg, mid)

def parallel(d: 'Line', p: 'Point'):
    """
    Returns a line parallel to the given line `d` that passes through the point `p`.

    Args:
        d (Line): The reference line.
        p (Point): The point through which the parallel line will pass.

    Returns:
        Line: A new Line object representing the parallel line.
    """
    
    lineVec = d.lineVec
    lineVec[2] = - lineVec[0] * p.x - lineVec[1] * p.y
    return Line(lineVec)

def angleBisector(*args):
    """ not complete (didn't find it is useful)"""
    if args == 2:
        line1, line2 = args
        cosa = np.inner(line1.lineVec, line2.lineVec) / (np.linalg.vector_norm(line1.lineVec) * np.linalg.vector_norm(line2.lineVec))
    ...
        
        
"""
class AngleBisector(Line):
    def __init__(self):
        super().__init__(p, q)

class AngleBisector(Line):
    def __init__(self, *args):
        if len(args) == 2 and all(isinstance(arg, Line) for arg in args):
            self.line1, self.line2 = args
            self._create_from_lines(self.line1, self.line2)
        elif len(args) == 3 and all(isinstance(arg, tuple) and len(arg) == 2 for arg in args):
            self.point1, self.point2, self.point3 = args
            self._create_from_points(self.point1, self.point2, self.point3)
        else:
            raise ValueError("Invalid arguments. Provide either two lines or three points.")

    def _create_from_lines(self, line1, line2):
        print(f"Creating AngleBisector from lines: {line1}, {line2}")

    def _create_from_points(self, point1, point2, point3):
        print(f"Creating AngleBisector from points: {point1}, {point2}, {point3}")"""


"""A = Point(1, 1)
B = Point(5, 5)
C = Point(5, 1)
D = Point(8, 8)
E = Point(3, 3)
F = Point(0, 0)

m = Segment(E, C)
n = perp_bisector(m)
print( n.lineVec, n)

m = Line(A, B)
n = perpendicular(m, D)
print( n.lineVec, n)

m = Line(A, B)
n = parallel(m, C)
print( n.lineVec, n)"""

