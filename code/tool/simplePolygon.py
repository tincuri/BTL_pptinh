import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from point import Point, midPoint # type: ignore
from construct import perpendicular, perp_bisector, parallel, angleBisector # type: ignore
from polygon import Polygon, SimplePolygon, lastPoint # type: ignore
from scipy.spatial import ConvexHull, convex_hull_plot_2d # type: ignore
from triangulate import triangulate

def newset(points: 'np.ndarray'):
    return [Point(_[0], _[1]) for _ in points]


# take input from test.txt
f = open("code/tool/dataset/case_20.txt", "r")

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
    array_for_hull = np.array([[_.coor()[0], _.coor()[1]] for _ in set], dtype=float)
    hull = ConvexHull(array_for_hull)

    # generate polygon
    vertices = newset(array_for_hull[hull.vertices]) # update polygon
    polygon = Polygon(vertices)

    # update set of points
    set = [_ for _ in set if _ not in vertices]

    # plot the convex hull for the first time
    #plotPolygon(polygon, array_for_hull, count=0)

    # get the list of new vertices can be inserted
    pos_vertices = makePosVer(set)

    return set, polygon, array_for_hull, pos_vertices

def makePosVer(set: 'list'):
    # get the list of new vertices can be inserted
    arr_tmp = np.array([[_.coor()[0], _.coor()[1]] for _ in set], dtype=float)
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
    # plt.savefig(f"code/tool/figure/simplepolygon/case_100_{count}.png")
    plt.show()

def vonglap(set, polygon, array_for_hull, pos_vertices):
    """ dang nghi recursive method"""

    newpolygon, newset = SimplePolygon(polygon, set, pos_vertices)
    #print(len(set),len(newset))
    count = 1
    #plotPolygon(newpolygon, array_for_hull, count)
    #print("Points remain: ", len(newset)) # for debug

    # make new posible vertices list:
    while len(newset) > 2:
        print("[current] len set = ", len(newset))
        if len(newset) == 9:
            print("debug")
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

    plotPolygon(polygon, array_for_hull, count) # if you want to plot the last figure
    return set, polygon
        


set, polygon, array_for_hull, pos_vertices = generateHull(set)
set, polygon = vonglap(set, polygon, array_for_hull, pos_vertices)



"""f = open("code/tool/15points_test.txt", "w")

for vertex in polygon.vertices:
    taolao = vertex.coor()
    a, b = taolao
    xau = str(a) + " " + str(b)
    f.write(xau)
    f.write("\n")"""

"""f = open("tool/go_triangulate_30p.txt", 'w')
for edge in polygon.edges:
    ax, ay = edge.px, edge.py
    
    bx, by = edge.qx, edge.qy
    xau = str(ax) + " " + str(ay) + " " + str(bx) + " " + str(by)
    f.write(xau)
    f.write("\n")"""

### NEW


#print(len(polygon.edges), len(polygon.vertices)) # check the return's of vonglap() function

#intersects = triangulate(polygon, array_for_hull)
#print(intersects)

















