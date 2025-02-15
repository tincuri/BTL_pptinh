import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from typing import Union

class Point:
    """
    Represents a point in the form (x, y).

    Attributes:
        x (float): The x-coordinate of the point.
        y (float): The y-coordinate of the point.
    
    Methods:
        __init__(self, x, y):
            Initializes a Point with coordinates x and y.
        
        __str__:
            Returns a string representation of the Point.
        
        __eq__:
            Checks equality of two Point objects.
        
        distance:
            Calculates the Euclidean distance to another Point.
        
        coor:
            Returns the coordinates as a numpy array.
    """
    def __init__(self, x: Union[int, float], y: Union[int, float]):
        self.x = float(x)
        self.y = float(y)
    
    def __str__(self) -> str:
        return str(f"({self.x}, {self.y})")
    
    def __eq__(self, other: 'Point') -> bool:
        """Check equality of two points."""
        epsilon = 1e-6

        if isinstance(other, Point):
            return (
                -epsilon <= self.x - other.x <= epsilon and
                -epsilon <= self.y - other.y <= epsilon
            )

        raise NotImplementedError("Comparison not supported between instances of different types.")

    def distance(self, other: 'Point') -> float:
        dist_sq = (self.x - other.x)**2 + (self.y - other.y)**2
        return np.sqrt(dist_sq)
    
    def coor(self) -> np.ndarray:
        """Returns the coordinates of the point as a ndarray."""
        return np.array([self.x, self.y], dtype=float)
    
    

    
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




    
"""A = Point(1, 2)
B = Point(7, 2)
c = A.distance(B)
print(c)
print(c)
print(A.coor()[0], A.coor(), type(A.coor()), A)

Q = Point(1,2)

listaa = [A, B]
if Q in listaa:
    print("true")"""


"""A = Point(1, 1)
B = Point(5, 5)
E = Point(3, 3)
F = Point(0, 0)
G = midPoint(A, B)
print(G.distance(A), G.distance(E))
print(G)"""
