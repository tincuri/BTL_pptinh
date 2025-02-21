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

"""# take input from test.txt
f = open("code/tool/diag.txt", "r")

# insert input points to list
set = [] # set of all points which hasn't become verticle
n = int(f.readline()) # number of diagonals
for i in range(n):
    coor = f.readline().split(' ')
    set.append((float(coor[0]), float(coor[1]))) # set of points 'Point'

# test case
# set.append((6, -1))
# set.append((3, -1))
# set.append((9, -2))"""


### READ FILE FROM C
### CURRENT STYLE: 
# --- LINE 1: NUMBER OF DIAGONAL
# --- LINE 2: SOURCE AND DESTINATION: xS yS xD yD (???)
# --- LINE 3 TO THE END: DIAG: xA yA xB yB (MAYBE FIX LATER DEPEND ON C OUTPUT FILE)

f = open("code/tool/finaltest.txt", "r")
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

# list of points (get from polygon/sleeve)
points = [(1, 5), (3,7), (4, 3), (5, 6), (6, 0), (6, 2), (9, 1), (9, 3), (10, 4), (12, 2), (11, 6), (13, 4), (13, 7)]

# polygon vertex
vertexes = [(1, 5), (3, 7), (5, 6), (6, 2), (9, 3), (10, 4), (11, 6), (13, 7), (13, 4), (12, 2), (9, 1), (6, 0), (4, 3), (1, 5)]



# RETURN TRUE IF A->B->C CCW, FALSE IF THEY'RE NOT
def isccw_x(a, b, c) -> bool:
    return (c[1]-a[1]) * (b[0]-a[0]) > (b[1]-a[1]) * (c[0]-a[0])

# plot the last time ( result ) # TWO IMAGE, FIRST WITH DIAGONALS, SECOND (RESULT) WITHOUT DIAGONALS
def lastplot(road: 'list', count: 'int'):
    plt.clf()

    # Polygon
    vertex_x = [vertex[0] for vertex in vertexes]
    vertex_y = [vertex[1] for vertex in vertexes]
    plt.plot(vertex_x, vertex_y, color='#000000', linestyle='-')

    # points and diag
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    plt.scatter(x, y, marker='p', color='blue')
    plt.plot(x, y, color='#000000', linestyle='--')

    # Shortest way
    x_road = [point[0] for point in road]
    y_road = [point[1] for point in road]
    plt.scatter(x_road, y_road, marker='s', color='black')
    plt.plot(x_road, y_road, color='red')
    #plt.savefig(f"code/tool/figure/lee/case_in_debug_{count}.png")
    #plt.show()



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
    #plt.savefig(f"code/tool/figure/lee/case_in_debug_{count}.png")

# PLOT TO INSERT TO THE REPORT
def plotTriangulate(upper: 'list', lower: 'list', road: 'list', count: 'int'):
    plt.clf()

    # Polygon
    vertex_x = [vertex[0] for vertex in vertexes]
    vertex_y = [vertex[1] for vertex in vertexes]
    plt.plot(vertex_x, vertex_y, color='#000000', linestyle='-')

    # points and diag
    x = [point[0] for point in points]
    y = [point[1] for point in points]
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
    #plt.savefig(f"code/tool/figure/lee/case_in_debug_{count}.png")
    #plt.show()



### MAIN LOGIC BEGIN
count = 0 # for save figure

# INITIAL
road = [points[0]] # list of cusp or final path
cusp = points[0] # LET source be the cusp
global_upper_branch = [points[0]]
global_lower_branch = [points[0]]

up_turn = None # store the turn of two convex (can be inferenced)
state = 1 # 1 mean to check from upper first, 0 mean to check from lower first

# GENERAL STEP

def general_step(diagonal: 'list', cusp: 'tuple', upper_branch: 'list', lower_branch: 'list', state: 'int'):
    linked = False # True if point is added
    if len(upper_branch) < 2 and len(lower_branch) < 2: # case: only contains cusp, state don't change
        upper_branch.insert(0, diagonal[0])
        lower_branch.insert(0, diagonal[1])
    elif len(upper_branch) < 2: # case new cusp is last point of lower_branch (but now it is upper(local))
        upper_branch.insert(0, diagonal[1])
        state = 1 - state # switch state
    else: # generally case
        # get the turn of two branch
        up_to_low = isccw_x(upper_branch[-2], cusp, lower_branch[-2])
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
                    state = 1 - state # switch state
                    linked = True # to break
                    break
                else:
                    upper_branch.insert(0, diagonal[1])
                    state = 1 - state
                    linked = True
                    break
            elif isccw_x(diagonal[1], upper_branch[index], upper_branch[index+1]) != up_turn: # this mean to ADD HERE
                if maybe == False:
                    maybe = True
        # cusp case aka u_n
        if linked == False: # this mean to check cusp case
            if isccw_x(diagonal[1], upper_branch[-2], cusp) == up_to_low:
                if isccw_x(diagonal[1], lower_branch[-2], cusp) != up_to_low:
                    upper_branch = [diagonal[1], cusp] # update upper branch
                    state = 1 - state # switch state
                    linked = True # to break
        # lower_branch
        if linked == False: # mean to check lower branch
            for index in range(-1, -len(lower_branch), -1):  # Iterate backwards from u(n+1) to u(0)
                if isccw_x(diagonal[1], lower_branch[index], lower_branch[index-1]) == up_turn: # this mean to ADD HERE
                    
                    cusp = lower_branch[index-1] # NEW CUSP
                    road.append(cusp) # save cusp
                    upper_branch = [diagonal[1], cusp]
                    del lower_branch[index:] # delete points from index->end (not include index)
                    state = 1 - state # switch state
                    linked = True # to break
                    break

    print("Upper: ", upper_branch)
    print("Lower: ", lower_branch)
    print("-----------------------------------------------")
    print("-----------------------------------------------")
    print("-----------------------------------------------")
    return cusp, upper_branch, lower_branch, state
            

for diagonal in diagonals: # check diagonal one by one
    print("Current diagonal: ", diagonal)
    if state == 1:
        cusp, global_upper_branch, global_lower_branch, state = general_step(diagonal, cusp, global_upper_branch, global_lower_branch, state)
    else: # state == 0:
        cusp, global_lower_branch, global_upper_branch, state = general_step(diagonal, cusp, global_lower_branch, global_upper_branch, state)
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














# out date code below
# for reference later (if any)

"""
if not initial == 3:
    cusp = set[0]
    road.append(cusp)
    upper_branch.append(set[0])
    lower_branch.append(set[0])
    upper_branch.insert(0, set[1])
    lower_branch.insert(0, set[2])
    set.remove(set[2])
    set.remove(set[1])
    set.remove(set[0])
    initial = 3

print("initial: ")
print(cusp, upper_branch, lower_branch)
# print(set, len(set))

plotTriangulate(upper_branch, lower_branch, road, count)
count += 1
lastAdd = 1 # 1: upper branch, 0: lower branch

def alg(cusp, upper_branch, lower_branch, i, lastAdd):
    linked = False
    for up_index in range(len(upper_branch)-1):
        if not isccw_x(set[i], upper_branch[up_index], upper_branch[up_index+1]):
            if up_index != 0:
                del upper_branch[0: up_index]
            upper_branch.insert(0, set[i])
            linked = True
            lastAdd = 1 - lastAdd
            break
        elif lastAdd == 0:
            if isccw_x(set[i], upper_branch[up_index], upper_branch[up_index+1]):
                if up_index != 0:
                    del upper_branch[0: up_index]
                upper_branch.insert(0, set[i])
                linked = True
                lastAdd = 1 - lastAdd
                break

    if linked == False:
        # cusp case:
        if isccw_x(set[i], cusp, lower_branch[-2]) == isccw_x(set[i], upper_branch[-2], cusp):
            print("cusp case")
            upper_branch = [set[i], cusp]
            
            lastAdd = 1 - lastAdd
        else: # second case
            # print("switch branch")
            for down_index in range(len(lower_branch)-2, 0, -1): # 0 -> loop continue until reach index 0, -1: backward                    
                if not isccw_x(set[i], lower_branch[down_index], lower_branch[down_index+1]):
                    if len(lower_branch) < 3: # add
                        lower_branch.insert(0, set[i])
                        linked = True
                        # lastAdd = 1 - lastAdd
                        break
                    if isccw_x(set[i], lower_branch[down_index+1], lower_branch[down_index+2]):
                        cusp = lower_branch[down_index+1] # new cusp
                        road.append(cusp)
                        upper_branch = [set[i], cusp] # new upper
                        del lower_branch[down_index+2:] # +2 due to lower_branch[down_index+2] now is new cusp
                        linked = True
                        # lastAdd = 1 - lastAdd
                        break
            if linked == False: # ensure that no bug
                lower_branch.insert(0, set[i])   
                # lastAdd = 1 - lastAdd
    return cusp, upper_branch, lower_branch, lastAdd


for i in range(len(set)):
    print("current point", set[i])
    if i == 4:
        pass
    if lastAdd == 1:
        cusp, upper_branch, lower_branch, lastAdd = alg(cusp=cusp, upper_branch=upper_branch, lower_branch=lower_branch, i=i, lastAdd=lastAdd)
    else: # swap lower with upper
        cusp, lower_branch, upper_branch, lastAdd = alg(cusp=cusp, upper_branch=lower_branch, lower_branch=upper_branch, i=i, lastAdd=lastAdd)

    print(cusp, upper_branch, lower_branch)
    plotTriangulate(upper_branch, lower_branch, road, count)
    count += 1




"""







"""for i in range(len(set)):
    print("current point", set[i])
    if count == 1:
        linked = False
        for up_index in range(len(upper_branch)-1):
            if not isccw_x(set[i], upper_branch[up_index], upper_branch[up_index+1]):
                if up_index != 0:
                    del upper_branch[0: up_index]
                upper_branch.insert(0, set[i])
                linked = True
                break
    
        if linked == False:
            # cusp case:
            if isccw_x(set[i], cusp, lower_branch[1]) == isccw_x(set[i], upper_branch[-2], cusp):
                print("cusp case")
                upper_branch = [set[i], cusp]
            else: # second case
                # print("switch branch")
                for down_index in range(len(lower_branch)-2):                    
                    if not isccw_x(set[i], lower_branch[down_index], lower_branch[down_index+1]):
                        if len(lower_branch) < 3: # add
                            lower_branch.append(set[i])
                            linked = True
                            break
                        if isccw_x(set[i], lower_branch[down_index+1], lower_branch[down_index+2]):
                            cusp = lower_branch[down_index+1] # new cusp
                            road.append(cusp)
                            upper_branch = [set[i], cusp] # new upper
                            del lower_branch[0: down_index+1]
                            linked = True
                            break
                if linked == False: # ensure that no bug
                    lower_branch.append(set[i])

    
    print(cusp, upper_branch, lower_branch)
    plotTriangulate(upper_branch, lower_branch, road, count)
    count += 1"""



