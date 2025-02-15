import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from point import Point, midPoint # type: ignore
from line import Line, Segment, Ray # type: ignore
from construct import perpendicular, perp_bisector, parallel, angleBisector # type: ignore
from circles import Circle # type: ignore
import sys
from typing import Union
import heapq
from polygon import Polygon, SimplePolygon, lastPoint # type: ignore
from scipy.spatial import ConvexHull, convex_hull_plot_2d # type: ignore

def newset(points: 'np.ndarray'):
    return [Point(_[0], _[1]) for _ in points]


# take input from test.txt
f = open("code/tool/test.txt", "r")

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

    #print("Verticles of polygon: ",len(polygon.vertices), "remain:", len(set)) # for debug
    #print("new of polygon: ", polygon.getNew_array())

    # plot the convex hull for the first time
    #plotPolygon(polygon, array_for_hull, count=0)

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
    # plt.savefig(f"code/tool/figure/case_100_{count}.png")
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
    #plotPolygon(newpolygon, array_for_hull, count)
    #print("Points remain: ", len(newset)) # for debug

    # make new posible vertices list:
    while len(newset) > 2:
        new_pos_vertices = makePosVer(newset)
        newpolygon, newset = SimplePolygon(polygon, newset, new_pos_vertices)
        #print("Points remain: ", len(newset)) # for debug
        count += 1
        #plotPolygon(newpolygon, array_for_hull, count)

    # method for 2 last:
    polygon, set = lastPoint(newpolygon, newset)
    count += 1
    #plotPolygon(polygon, array_for_hull, count)
    if len(set) == 0:
        print("Generate Simple polygon successfully.")

    return set, polygon
        


set, polygon, array_for_hull, pos_vertices = generateHull(set)
#while len(set) > 0:
set, polygon = vonglap(set, polygon, array_for_hull, pos_vertices)


print(polygon.vertices)

f = open("code/tool/15points_test.txt", "w")

for vertex in polygon.vertices:
    taolao = vertex.coor()
    a, b = taolao
    xau = str(a) + " " + str(b)
    f.write(xau)
    f.write("\n")


### NEW


#print(len(polygon.edges), len(polygon.vertices)) # check the return's of vonglap() function

#intersects = triangulate(polygon, array_for_hull)
#print(intersects)


"""y_coor_list = [{"Point": vertex, "y_coor": float(vertex.y)} for vertex in polygon.vertices]
sorted_y_coor_list = sorted(y_coor_list, key=lambda item: item["y_coor"])
#print(sorted_y_coor_list)

# STEP 1:
if len(y_coor_list) <= 2:
    print("There are no visible pairs to compute.")

cur_point = y_coor_list[1].get("Point")
d = Line([0, 1, -cur_point.y])

print(d.lineVec[2], cur_point, d.lineVec)


# STEP 2:
### wrong way
list_intersects = []
for edge in polygon.edges:
    a, b, c = d.lineVec
    A, B, C = edge.lineVec
    
    x_intersect = edge.lineVec[1] * d.lineVec[2] - edge.lineVec[2]
    y_intersect = - d.lineVec[2]
    
    point_intersect = Point(x_intersect, y_intersect)
    if 0 < x_intersect < 1 and 0 < y_intersect < 1:
        if edge.onSegment(point_intersect) and point_intersect != cur_point:
            list_intersects.append(point_intersect)
            print(d.lineVec, edge.lineVec, x_intersect, y_intersect)

print("List_intersects: ", list_intersects)

aqaq = [[_.coor()[0], _.coor()[1]] for _ in list_intersects]
aqqqq = np.array(aqaq)

x_in = aqqqq[:, 0]
y_in = aqqqq[:, 1]

plt.scatter(x_in, y_in, marker='s')  # Create the scatter plot
#plt.plot(x_in, y_in, 'o')"""






















"""arr = polygon.getNew_array()
arr = np.vstack((arr, arr[0]))

plt.xlim(0, 1)  # Set x-axis limits from 2 to 8
plt.ylim(0, 1) # Set y-axis limits from -1.2 to 1.2

plt.plot(array_for_hull[:, 0], array_for_hull[:, 1], 'o')
plt.plot(arr[:, 0], arr[:, 1], 'r--', lw=2)

# x_line = np.linspace(0, 1, len(arr[:, 0]))
# y_line = np.full_like(x_line, np.float64(cur_point.y))

# print(x_line)
# print(y_line)
#plt.plot(x_line, y_line, label='y=0.8')


plt.show()
"""
















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















