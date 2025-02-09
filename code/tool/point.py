import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from typing import Union

class Point(object):
    """
    Represents a point in the form (x, y).

    Attributes:
        x (float): The x-coordinate of the point.
        y (float): The y-coordinate of the point.

    Methods:
        __init__(self, x: Union[int, float], y: Union[int, float]):
            Initializes a Point object with coordinates x and y.
        
        __str__(self) -> str:
            Returns a string representation of the Point object.

        __eq__(self, other: 'Point') -> bool:
            Checks if two Point objects are equal within a tolerance.

        distance(self, other: 'Point') -> Union[int, float]:
            Calculates the Euclidean distance between this Point and another Point.
        
        coor(self) -> Tuple[float, float]:
            Returns the coordinates of the point as a tuple.
        """
    def __init__(self, x: Union[int, float], y: Union[int, float]):
        self.x = x
        self.y = y
    
    def __str__(self):
        return str(f"({self.x}, {self.y})")
    
    def __eq__(self, other: 'Point') -> bool:
        """Check equality of two points."""
        epsilon = 1e-6

        if isinstance(other, Point):
            return (
                -epsilon <= np.float64(self.x) - np.float64(other.x) <= epsilon and
                -epsilon <= np.float64(self.y) - np.float64(other.y) <= epsilon
            )

        raise NotImplementedError()

    def distance(self, other: 'Point') -> Union[int, float]:
        dist_sq = (float(self.x) - float(other.x))**2 + (float(self.y) - float(other.y))**2
        return np.sqrt(dist_sq)
    
    def coor(self):
        """Returns the coordinates of the point as a tuple."""
        return (float(self.x), float(self.y))
    
    

    
def midPoint(p, q):
    """Represents mid point of p and q.

    Arguments:
        p (Point), y (Point)
                   
    Return:
        mid point at (x, y): Point(x, y)
    """ 
    px, py = p.coor()
    qx, qy = q.coor()
    x = (px + qx) / 2
    y = (py + qy) / 2
    return Point(x, y)


"""def __eq__(self, other: 'Point') -> bool:
    # Check equality of two points.
    epsilon = 1e-6
    if isinstance(other, Point):
        if -epsilon <= float(self.x) - float(other.x) <= epsilon:
            if -epsilon <= float(self.y) - float(other.y) <= epsilon:
                return True
        
        return (
            -epsilon <= float(self.x) - float(other.x) <= epsilon and
            -epsilon <= float(self.y) - float(other.y) <= epsilon
        )
    return False

    raise NotImplementedError()"""

    
"""A = Point(1, 2)
B = Point(7, 2)
c = A.distance(B)
print(c)
print(c)
print(A.coor()[0])"""

"""
A = Point(1, 1)
B = Point(5, 5)
E = Point(3, 3)
F = Point(0, 0)
G = Midpoint(A, B)
print(G.distance(A), G.distance(E))
print(G)
"""