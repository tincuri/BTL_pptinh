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
f = open("code/tool/case_1000.txt", "r")

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
#plt.savefig(f"code/tool/figure/triangulation/case_100_0.png")
#plt.show() # show origin simple polygon


def plotTriangulate(for_plot: 'tuple', count: 'int'):
    plt.scatter(x_in, y_in, marker='o', color='blue')  # Create the scatter plot
    plt.plot(arr[:, 0], arr[:, 1], 'r--', lw=2)
    for diagonal in for_plot:
        x_values, y_values = diagonal
        plt.plot(x_values, y_values, 'k-', lw=2)
    #plt.savefig(f"code/tool/figure/triangulation/case_100_{count}.png")
    #plt.show() # show origin simple polygon

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
    a, b, c = map(np.array, [_.coor() for _ in triangle])
    p = np.array(p.coor())

    def cross(v1, v2):
        return np.cross(v1, v2)
    
    return all((cross(b - a, p - a) >= 0, cross(c - b, p - b) >= 0, cross(a - c, p - c) >= 0)) or \
           all((cross(b - a, p - a) <= 0, cross(c - b, p - b) <= 0, cross(a - c, p - c) <= 0))

def makeMonotone(polygon: 'Polygon'): # a: 'List' --> queue = [vertex: 'Point', "type of vertex": 'str']
    final_triangles = []
    diags = []
    vertices = polygon.vertices.copy()
    original_vertices = polygon.vertices.copy()

    line_inserted = 0

    triangles_found = -1
    for_plot = [] # array for plot
    while triangles_found != 0:
        triangles_found = 0

        for index in range(len(vertices)):
            vertex = vertices[index]
            prev_ver = vertices[index - 1]
            try:
                next_ver = vertices[index + 1]
            except IndexError: # handle last index
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
                    for_plot.append((x_values, y_values))
                    
                    line_inserted += 1
                    #plotTriangulate(for_plot, line_inserted)

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
    return diags#, final_triangles
    


#triangles = makeMonotone(polygon)
list_of_vertex = polygon.vertices
diagonals = makeMonotone(polygon)
forldm = [] # contain (i_a, i_b) are index of each diagonal
for diagonal in diagonals:
    first = list_of_vertex.index(diagonal[0])
    second = list_of_vertex.index(diagonal[1])
    forldm.append((first, second))
print(forldm)
# write txt for C code

"""f = open("code/tool/15points_testt.txt", "w")

for triangle in triangles:
    a, b, c = triangle
    xau = str((a.coor()[0], a.coor()[1])) + " " + str((c.coor()[0], c.coor()[1])) + " " + str((b.coor()[0], b.coor()[1]))
    f.write(xau)
    f.write("\n")"""



#print(triangles)

































"""f = open("code/tool/15points_test.txt", "w")

for triangle in triangles:
    pre_ver, ver, nex_ver = triangle

    xau = str(pre_ver.coor()) + " " + str(ver.coor()) + " " + str(nex_ver.coor())
    f.write(xau)
    f.write("\n")
"""

































