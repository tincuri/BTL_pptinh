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
import math




# take input from test.txt
f = open("code/tool/15points.txt", "r")

# insert input points to list
set = [] # set of all points which hasn't become verticle
n = int(f.readline())
for i in range(n):
    coor = f.readline().split(' ')
    set.append(Point(coor[0], coor[1].replace('\n', ""))) # set of points 'Point'

polygon = Polygon(set)


aqaq = np.array([[_.coor()[0], _.coor()[1]] for _ in polygon.vertices])

x_in = aqaq[:, 0]
y_in = aqaq[:, 1]

# plot
arr = polygon.getNew_array()
arr = np.vstack((arr, arr[0]))
plt.scatter(x_in, y_in, marker='o')  # Create the scatter plot
#plt.plot(array_for_hull[:, 0], array_for_hull[:, 1], 'o')
plt.plot(arr[:, 0], arr[:, 1], 'r--', lw=2)


abccc = polygon.verticesType()
list_of_edges = polygon.edges
#for _ in a:
    #print(_[0], _[1])
    #print(type(_[0].y))

# now: success classified vertices into 5 groups
# then: generate monotone polygon aka monopoly


def sortQueue(a: 'list')->list:
    """
    Return list of index from 0 -> n-1
    """
    a_origin = a.copy() # copy for check index
    a_sorted = [] # sort by smallest first, use selection sort
    while len(a) > 0:
        min_a = 0
        for _ in a:
            if min_a == 0 or _[0].y < min_a:
                min_a = _[0].y
                element = _
                for ele in a_origin:
                    if element == ele:
                        i = a_origin.index(ele)
        a_sorted.append(i) 
        a.remove(element)
    a_reverse = a_sorted[::-1]
    return a_reverse, a_origin
    
def isInside(triangle: 'tuple', p: 'Point') -> bool:
    a, b, c = triangle
    a, b, c, p = map(np.array, [a.coor(), b.coor(), c.coor(), p.coor()])

    # calculate vectors
    ab = b - a
    ap = p - a
    bc = c - b
    bp = p - b
    ca = a - c
    cp = p - c

    # cross product
    cross1 = np.cross(ab, ap)
    cross2 = np.cross(bc, bp)
    cross3 = np.cross(ca, cp)
    return (cross1 >= 0 and cross2 >= 0 and cross3 >= 0) or (cross1 <= 0 and cross2 <= 0 and cross3 <= 0)

def makeMonotone(polygon: 'Polygon'): # a: 'List' --> queue = [vertex: 'Point', "type of vertex": 'str']
    final_triangles = []
    diags = []
    vertices = polygon.vertices.copy()
    original_vertices = polygon.vertices.copy()

    line_inserted = 0

    triangles_found = -1
    while triangles_found != 0:
        #print("here", len(vertices), vertices[0])
        triangles_found = 0

        for index in range(len(vertices)):
            vertex = vertices[index]
            prev_ver = vertices[index - 1]
            try:
                next_ver = vertices[index + 1]
            except IndexError:
                next_ver = vertices[0]

            #print(prev_ver, vertex, next_ver)
            try:
                angle = polygon.newangle(prev_ver, vertex, next_ver)
            except ValueError:
                break
            if not angle >= math.pi:
                triangle = (prev_ver, vertex, next_ver)
                points = [p for p in original_vertices if p not in triangle]

                inside = [isInside(triangle, point) for point in points]

                if not any(inside):
                    final_triangles.append(triangle)

                    stacked = np.stack((np.array([prev_ver.x, prev_ver.y]) , np.array([next_ver.x, next_ver.y])))
                    x_values = stacked[:, 0]  # Get [a, c]
                    y_values = stacked[:, 1]  # Get [b, d]
                    plt.plot(x_values, y_values, 'b-', lw=2)
                    line_inserted += 1

                    diags.append((prev_ver, next_ver))

                    vertices.pop(index)
                    triangles_found += 1
                    break
        
        # Check for infinite loop
        if triangles_found == 0:
            print(f"Loop detected. Exiting. found {len(final_triangles)} triangles")
            break
    #print(diags)
    print("Lines will be inserted: ", line_inserted)
    return final_triangles
    


triangles = makeMonotone(polygon)


plt.show()



f = open("code/tool/15points_test.txt", "w")

for triangle in triangles:
    pre_ver, ver, nex_ver = triangle

    xau = str(pre_ver.coor()) + " " + str(ver.coor()) + " " + str(nex_ver.coor())
    f.write(xau)
    f.write("\n")





































"""
def old_makeMonotone(a:'list'): # a: 'List' --> queue = [vertex: 'Point', "type of vertex": 'str']
    tree = [{"edge": 0, "helper": 0, "style": None} for _ in a] # tree: edge and helper of edge
    #print(tree)

    def handleStartVertex(vertex: 'Point', index: 'int'):
        tree[index] = {"edge": list_of_edges[index], "helper": vertex, "style": "start"}
        #print(tree[0].get("edge").p, tree[0].get("edge").q, tree[0].get("helper"))

    def handleEndVertex(vertex: 'Point', index: 'int'):
        if tree[index-1].get("style") == "merge": #or tree[index-1].get("style") != None:
            pass # insert diagonal 
        tree[index-1] = {"edge": 0, "helper": 0, "style": None}
    
    def handleSplitVertex(vertex: 'Point', index: 'int'):
        ...

    # queqe Q sort by y-coor:
    priority_queue, a = sortQueue(a)
    while len(priority_queue) > 0:
        vertex, vertex_type = a[priority_queue[0]]
        # print(type(vertex), vertex, vertex_type)
        if vertex_type == "start":
            handleStartVertex(vertex, priority_queue[0])
        #elif vertex_type == "end":
        #    handleEndVertex()
        print(tree, priority_queue[0])
        break
    # handle cases

"""