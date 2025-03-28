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


### READ FILE FROM C
### CURRENT STYLE: 
# --- LINE 1: NUMBER OF DIAGONAL
# --- LINE 2: SOURCE AND DESTINATION: xS yS xD yD (???)
# --- LINE 3 TO THE END: DIAG: xA yA xB yB (MAYBE FIX LATER DEPEND ON C OUTPUT FILE)

f = open("./tool/ldm.txt", "r")
diagonals = []
n = int(f.readline())
for i in range(n):
    if i == 0:
        coor = f.readline().split(' ')
        source = (float(coor[0]), float(coor[1]))
        destination = (float(coor[2]), float(coor[3]))
    else:
        coor = f.readline().split(' ')
        first = (float(coor[0]), float(coor[1]))
        second = (float(coor[2]), float(coor[3]))
        diagonals.append([first, second])


### ASSUME THAT WE HAVE A POLYGON HERE (BUT NOW WE HAVEN'T)

# take diagonals (for plot)
plot_diag = diagonals.copy()

# polygon vertex
vertexes = [(0.0774155313078, 0.8113376396024), (0.0681084508445, 0.4855898233843), (0.2011792554782, 0.2525821297921), (0.0805178914623, 0.0977948040772), (0.356627945209, 0.1008971642316), (0.5041553935497, 0.3536057313367), (0.5489742747854, 0.109873562687), (0.7816512863697, 0.1288184056217), (0.7382182442073, 0.5263142984417), (0.8530055699222, 0.5380308195229), (0.8933362519302, 0.1195113251584), (0.9522810948648, 0.4049284593684), (0.8530055699222, 0.693447953733), (0.6917459529319, 0.6624243521884), (0.3162972632011, 0.7927234786756), (0.1859981367139, 0.6314007506438), (0.4935255850546, 0.6596842295626), (0.2914783819654, 0.4521567812219), (0.1704863359416, 0.4321567825897), (0.0774155313078, 0.8113376396024)] # 15 points test case



### FUNCTION

# RETURN TRUE IF A->B->C CCW, FALSE IF THEY'RE NOT
def isccw_x(a, b, c):
    return (c[1]-a[1]) * (b[0]-a[0]) > (b[1]-a[1]) * (c[0]-a[0])

# plot the last time ( result ) # TWO IMAGE, FIRST WITH DIAGONALS, SECOND (RESULT) WITHOUT DIAGONALS
def lastplot(road: 'list', count: 'int'):
    plt.clf()

    # Polygon
    vertex_x = [vertex[0] for vertex in vertexes]
    vertex_y = [vertex[1] for vertex in vertexes]
    plt.plot(vertex_x, vertex_y, color='#000000', linestyle='-')

    # points and diag
    x = []
    y = []
    for diag in plot_diag:
        x = [point[0] for point in diag]
        y = [point[1] for point in diag]
        plt.scatter(x, y, marker='p', color='blue')
        plt.plot(x, y, color='#000000', linestyle='--')

    # Shortest way
    x_road = [point[0] for point in road]
    y_road = [point[1] for point in road]
    plt.scatter(x_road, y_road, marker='s', color='black')
    plt.plot(x_road, y_road, color='red')
    #plt.savefig(f"code/tool/figure/lee/example2/example_2_{count}.png")
    plt.show()



    # no diag
    count += 1
    plt.clf()

    # Polygon
    vertex_x = [vertex[0] for vertex in vertexes]
    vertex_y = [vertex[1] for vertex in vertexes]
    plt.plot(vertex_x, vertex_y, color='#000000', linestyle='-')

    # Shortest way
    x_road = [point[0] for point in road]
    y_road = [point[1] for point in road]
    plt.scatter(x_road, y_road, marker='s', color='black')
    plt.plot(x_road, y_road, color='red')
    #plt.savefig(f"code/tool/figure/lee/example2/example_2_{count}.png")
    plt.show

# PLOT TO INSERT TO THE REPORT
def plotTriangulate(upper: 'list', lower: 'list', road: 'list', count: 'int'):
    plt.clf()

    # Polygon
    vertex_x = [vertex[0] for vertex in vertexes]
    vertex_y = [vertex[1] for vertex in vertexes]
    plt.plot(vertex_x, vertex_y, color='#000000', linestyle='-')

    # points and diag
    x = []
    y = []
    for diag in plot_diag:
        x = [point[0] for point in diag]
        y = [point[1] for point in diag]
        plt.scatter(x, y, marker='p', color='blue')
        plt.plot(x, y, color='#000000', linestyle='--')

    # Upper branch
    x_up = [point[0] for point in upper]
    y_up = [point[1] for point in upper]
    plt.scatter(x_up, y_up, marker='o', color='blue')
    plt.plot(x_up, y_up, color='#1f77b4')
    # Lower branch
    x_down = [point[0] for point in lower]
    y_down = [point[1] for point in lower]
    plt.scatter(x_down, y_down, marker='o', color='red')
    plt.plot(x_down, y_down, color='#ff8a23')
    # Shortest way
    x_road = [point[0] for point in road]
    y_road = [point[1] for point in road]
    plt.scatter(x_road, y_road, marker='s', color='black')
    plt.plot(x_road, y_road, color='red')
    #plt.savefig(f"code/tool/figure/lee/example2/example_2_{count}.png")
    plt.show()



### MAIN LOGIC BEGIN
count = 0 # for save figure

# INITIAL
road = [source] # list of cusp or final path
cusp = source # LET source be the cusp
global_upper_branch = [source]
global_lower_branch = [source]

up_turn = None # store the turn of two convex (can be inferenced)

# GENERAL STEP

def general_step(diagonal: 'list', cusp: 'tuple', upper_branch: 'list', lower_branch: 'list'):
    linked = False # True if point is added
    if len(upper_branch) < 2 and len(lower_branch) < 2: # case: only contains cusp, state don't change
        upper_branch.insert(0, diagonal[0])
        lower_branch.insert(0, diagonal[1])
    elif len(upper_branch) < 2: # case new cusp is last point of lower_branch (but now it is upper(local))
        upper_branch.insert(0, diagonal[1])
        linked = True
    else: # generally case
        # get the turn of two branch
        try: # handle case len(lower_branch) = 0
            up_to_low = isccw_x(upper_branch[-2], cusp, lower_branch[-2])
        except IndexError:
            up_to_low = isccw_x(upper_branch[-2], cusp, cusp)
        if up_to_low: # up_to_low is true = ccw
            up_turn = False # up_turn nguoc chieu -> cw
        else:
            up_turn = True
        
        # check upper_branch first:
        maybe = False # check if maybe can be added or not
        for index in range(len(upper_branch)-1): # u_0 to u_(n-1)
            if isccw_x(diagonal[1], upper_branch[index], upper_branch[index+1]) == up_turn: # this mean to ADD HERE
                if maybe == True: # this mean you need to delete some point
                    del upper_branch[:index] # delete points from 0->index-1 (not include index)
                    upper_branch.insert(0, diagonal[1])
                    linked = True # to break
                    break
                else:
                    upper_branch.insert(0, diagonal[1])
                    linked = True
                    break
            elif isccw_x(diagonal[1], upper_branch[index], upper_branch[index+1]) != up_turn: # this mean to ADD HERE
                if maybe == False:
                    maybe = True
        # cusp case aka u_n
        if linked == False: # this mean to check cusp case
            if len(lower_branch) < 2:
                upper_branch = [diagonal[1], cusp]
                linked = True
            elif isccw_x(diagonal[1], upper_branch[-2], cusp) == up_to_low:
                if isccw_x(diagonal[1], lower_branch[-2], cusp) != up_to_low:
                    upper_branch = [diagonal[1], cusp] # update upper branch
                    linked = True # to break
        # lower_branch
        if linked == False: # mean to check lower branch 
            for index in range(-1, -len(lower_branch), -1):  # Iterate backwards from u(n+1) to u(0)
                if isccw_x(diagonal[1], lower_branch[index], lower_branch[index-1]) == up_turn: # this mean to ADD HERE
                    cusp = lower_branch[index-1] # NEW CUSP
                    road.append(cusp) # save cusp
                    upper_branch = [diagonal[1], cusp]
                    del lower_branch[index:] # delete points from index->end (not include index)
                    linked = True # to break
                    break
    if linked == False:
        print("FAIL!!!")
    return cusp, upper_branch, lower_branch
            
timesss = 0
for diagonal in diagonals: # check diagonal one by one
    #print("Current diagonal: ", diagonal)
    if timesss == 0: # initial case
            global_upper_branch.insert(0, diagonal[0])
            global_lower_branch.insert(0, diagonal[1])
            timesss += 1

    if diagonal[0] == global_upper_branch[0] or diagonal[1] == global_upper_branch[0]: # this mean upper branch has reach current diagonal no need to change
        # so we check lower branch first
        cusp, global_lower_branch, global_upper_branch = general_step(diagonal, cusp, global_lower_branch, global_upper_branch)
    elif diagonal[0] == global_lower_branch[0] or diagonal[1] == global_lower_branch[0]:
        cusp, global_upper_branch, global_lower_branch = general_step(diagonal, cusp, global_upper_branch, global_lower_branch)
    else: # case only contain cusp or FAIL:
        if len(global_upper_branch) == 1 and len(global_lower_branch) == 1: # ensure not FAIL
            global_upper_branch.insert(0, diagonal[0])
            global_lower_branch.insert(0, diagonal[1])

        else:
            print("yowaimushi")
    plotTriangulate(upper=global_upper_branch, lower=global_lower_branch, road=road, count=count)
    count += 1

# final step:
if destination in global_upper_branch:
    for _ in reversed(global_upper_branch):
        if _ not in road:
            road.append(_)
else:
    for _ in reversed(global_lower_branch):
        if _ not in road:
            road.append(_)
print("road: ", road)
lastplot(road, count)