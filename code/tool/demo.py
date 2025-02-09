import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from point import Point, midPoint # type: ignore
from line import Line, Segment, Ray # type: ignore
from construct import perpendicular, perp_bisector, parallel, angleBisector # type: ignore
from circles import Circle # type: ignore
import sys
from typing import Union
import heapq
from polygon import Polygon, SimplePolygon # type: ignore
from scipy.spatial import ConvexHull, convex_hull_plot_2d # type: ignore

def newset(points: 'np.ndarray'):
    return [Point(_[0], _[1]) for _ in points]


# take input from test.txt
f = open("tool/test.txt", "r")

# insert input points to list
set = [] # set of all points which hasn't become verticle
n = int(f.readline())
for i in range(n):
    coor = f.readline().split(' ')
    set.append(Point(coor[0], coor[1].replace('\n', ""))) # set of points 'Point'

def generateHull(set: 'list') -> tuple:
    """Generates the initial convex hull polygon and updates the point set.

    Constructs the initial polygon from the convex hull of the input point set.
    Updates the set by removing the hull vertices.

    Args:
        set (list): A list of Point objects.

    Returns:
        tuple: A tuple containing the updated set, the initial polygon, the array for hull, and the possible vertices.
    """

    # initialize the polygon as a convex hull of the points
    array_for_hull = np.ndarray(shape=(n, 2), dtype=float)
    array_for_hull[:] = [[float(_.coor()[0]), float(_.coor()[1])] for _ in set]
    hull = ConvexHull(array_for_hull)

    # generate polygon
    vertices = newset(array_for_hull[hull.vertices]) # update polygon
    polygon = Polygon(vertices)

    # update set of points
    set = [_ for _ in set if _ not in vertices] # update set

    print("Verticles of polygon: ",len(polygon.vertices), "remain:", len(set))
    #print("new of polygon: ", polygon.getNew_array())

    # plot the convex hull for the first time
    plotPolygon(polygon, array_for_hull, count=0)

    # get the list of new vertices can be inserted
    arr_tmp = np.ndarray(shape=(len(set), 2), dtype=float)
    arr_tmp[:] = [[float(_.coor()[0]), float(_.coor()[1])] for _ in set]
    hull_tmp = ConvexHull(arr_tmp)
    pos_vertices = newset(arr_tmp[hull_tmp.vertices]) # list of posible vertices ( array of Point )
    """for _ in pos_vertices:
        print(_)
    for _ in set:
        print("set: ", _)"""
    return set, polygon, array_for_hull, pos_vertices

def makePosVer(set: 'list'):
    # get the list of new vertices can be inserted
    arr_tmp = np.ndarray(shape=(len(set), 2), dtype=float)
    arr_tmp[:] = [[float(_.coor()[0]), float(_.coor()[1])] for _ in set]
    hull_tmp = ConvexHull(arr_tmp)
    pos_vertices = newset(arr_tmp[hull_tmp.vertices]) # list of posible vertices ( array of Point )
    return pos_vertices


def plotPolygon(polygon, array_for_hull, count: 'int'):
    """For plot.

    Args:
        polygon (Polygon)
        array_for_hull (ndarray): to print all the points
        count : to save figures

    Returns:
        nothing
    """
    arr = polygon.getNew_array()
    arr = np.vstack((arr, arr[0]))
    plt.plot(array_for_hull[:, 0], array_for_hull[:, 1], 'o')
    plt.plot(arr[:, 0], arr[:, 1], 'r--', lw=2)
    plt.savefig(f"tool/figure/case_100_{count}.png")
    plt.show()

"""def vonglap(set, polygon, array_for_hull):
    newpolygon, newset = SimplePolygon(polygon, set)
    #print("Verticles of polygon: ",len(newpolygon.vertices), len(newset), len(newpolygon.new_array))
    #print("new of polygon: ", newpolygon.getNew_array())
    print(len(set),len(newset))
    #plotPolygon(newpolygon, array_for_hull)

    newpolygon, newset = SimplePolygon(newpolygon, newset)
    print(len(set),len(newset))
    #plotPolygon(newpolygon, array_for_hull)

    newpolygon, newset = SimplePolygon(newpolygon, newset)
    print(len(set),len(newset))
    plotPolygon(newpolygon, array_for_hull)

    newpolygon, newset = SimplePolygon(newpolygon, newset)
    print(len(set),len(newset))
    plotPolygon(newpolygon, array_for_hull)

    newpolygon, newset = SimplePolygon(newpolygon, newset)
    print(len(set),len(newset))
    plotPolygon(newpolygon, array_for_hull)"""

"""def vonglap(set, polygon, array_for_hull):
    i = 0
    if i == 0:
        newpolygon, newset = SimplePolygon(polygon, set)
        i += 1
    
    while len(set) > 0:
        if i == 2:
            print("debug")
        newpolygon, newset = SimplePolygon(newpolygon, newset)
        print(len(set),len(newset))
        plotPolygon(newpolygon, array_for_hull)
        i += 1
    # skip
    newpolygon, newset = vonglap(newset, polygon, array_for_hull)
    print(len(set),len(newset))
    plotPolygon(newpolygon, array_for_hull)
    if len(set) == 0:
        return newpolygon, newset"""

def vonglap(set, polygon, array_for_hull, pos_vertices):
    """ dang nghi recursive method"""

    newpolygon, newset = SimplePolygon(polygon, set, pos_vertices)
    #print(len(set),len(newset))
    count = 1
    plotPolygon(newpolygon, array_for_hull, count)
    print("Points remain: ", len(newset))

    # make new posible vertices list:
    while len(newset) > 2:
        new_pos_vertices = makePosVer(newset)
        newpolygon, newset = SimplePolygon(polygon, newset, new_pos_vertices)
        print("Points remain: ", len(newset))
        count += 1
        plotPolygon(newpolygon, array_for_hull, count)
        
        



set, polygon, array_for_hull, pos_vertices = generateHull(set)
#while len(set) > 0:
vonglap(set, polygon, array_for_hull, pos_vertices)
















"""plt.plot(array_for_hull[:,0], array_for_hull[:,1], 'o')
plt.plot(array_for_hull[hull.vertices,0], array_for_hull[hull.vertices,1], 'r--', lw=2)
plt.show()"""

#print("test: ", array_for_hull[hull.vertices,0], polygon.new_array[:, 0])


"""polygon, set = SimplePolygon(polygon, set)
print("Verticles of polygon: ",len(polygon.vertices), len(set), len(polygon.new_array))
print("new of polygon: ", polygon.getNew_array())

arr = polygon.getNew_array()
#print(arr)
#new_row =   # The row you want to add
arr = np.vstack((arr, arr[0]))

plt.plot(arr[:, 0], arr[:, 1], 'o')
plt.plot(arr[:, 0], arr[:, 1], 'r--', lw=2)
plt.show()
"""





















#for _ in set:
#    print(_)

#polygon = Polygon(quickhull(points))

# update points set to exclude polygon vertices
#points = [x for x in points if x not in polygon.vertices]
#print(type(set[0]), set[0])