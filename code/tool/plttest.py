import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from polygon import Polygon # type: ignore
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from point import Point # type: ignore

# ============================================================================================
#              This file takes C output sleeve (already has simple polygon) => Lee alg
# ============================================================================================


# ==============================================
#              SIMPLE POLYGON
# ==============================================

# take input from test.txt
f = open("code/tool/nds/maze.txt", "r")

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
#plt.savefig(f"code/tool/figure/lee/example3/example_3.png")
#plt.show() # show origin simple polygon






# ==============================================
#              SLEEVE
# ==============================================

f = open("code/tool/nds/maze_sleeve.txt", "r")
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


# list of points (get from polygon/sleeve)
plot_diag = diagonals.copy() # for plot

# polygon vertex
vertexes = polygon.getNew_array()
vertexes = np.vstack([vertexes, vertexes[0]]) 




# ==============================================
#              FUNCTION
# ==============================================


# RETURN TRUE IF A->B->C CCW, FALSE IF THEY'RE NOT
def isccw_x(a, b, c):
    # handle straight case
    #if (a[0] - b[0]) * (a[1] - c[1])  == (a[1] - b[1]) * (a[0] - c[0]) :
    #    return "straight" # false if straight
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
    #plt.savefig(f"code/tool/figure/lee/example3/example_3_{count}.png")
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
    #plt.savefig(f"code/tool/figure/lee/example3/example_3_{count}.png")
    #plt.show()

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
    #plt.savefig(f"code/tool/figure/lee/example3/example_3_{count}.png")
    #plt.show()




# ==============================================
#              MAIN LOGIC BEGIN
# ==============================================

count = 0 # for save figure


# ==============================================
#              INITIAL STEP
# ==============================================

road = [source] # list of cusp or final path
cusp = source # LET source be the cusp
global_upper_branch = [source]
global_lower_branch = [source]

up_turn = None # store the turn of two convex (can be inferenced)




# ==============================================
#              GENERAL STEP
# ==============================================

def general_step(insertP: 'Point', diagonal: 'list', cusp: 'tuple', upper_branch: 'list', lower_branch: 'list'):
    linked = False # True if point is added
    if len(upper_branch) < 2 and len(lower_branch) < 2: # case: only contains cusp, state don't change
        upper_branch.insert(0, diagonal[0])
        lower_branch.insert(0, diagonal[1])


    elif len(upper_branch) < 2: # case new cusp is last point of lower_branch (but now it is upper(local))
        upper_branch.insert(0, insertP)
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
            if isccw_x(insertP, upper_branch[index], upper_branch[index+1]) == up_turn:
                del upper_branch[:index] # delete points from 0->index-1 (not include index)
                upper_branch.insert(0, insertP)
                linked = True # to break
                break

        # cusp case aka u_n
        if linked == False: # this mean to check cusp case

            if len(lower_branch) < 2:
                upper_branch = [insertP, cusp]
                linked = True
            elif isccw_x(insertP, upper_branch[-2], cusp) == up_to_low:
                if isccw_x(insertP, lower_branch[-2], cusp) != up_to_low:
                    upper_branch = [insertP, cusp] # update upper branch
                    linked = True # to break
        # lower_branch
        if linked == False: # mean to check lower branch 
            for index in range(-1, -len(lower_branch), -1):  # Iterate backwards from u(n+1) to u(0)
                def sub_isccw_x(a, b, c): # return straight or not
                    return (c[1]-a[1]) * (b[0]-a[0]) == (b[1]-a[1]) * (c[0]-a[0])
                
                if isccw_x(insertP, lower_branch[index], lower_branch[index-1]) != up_turn and index != -1:
                    for _ in reversed(lower_branch):
                        if _ not in road:
                            road.append(_)
                            if _ == lower_branch[index]: # NEW CUSP
                                cusp = lower_branch[index]

                                upper_branch = [insertP, cusp]
                                del lower_branch[index+1:] # delete points from index->end (not include index)
                                linked = True # to break
                                break
                    if linked: break


                elif sub_isccw_x(insertP, lower_branch[index], lower_branch[index-1]) :
                    for _ in reversed(lower_branch):
                        if _ not in road:
                            road.append(_)
                            if _ == lower_branch[index-1]: # NEW CUSP
                                cusp = lower_branch[index-1]

                                upper_branch = [insertP, cusp]
                                del lower_branch[index:] # delete points from index->end (not include index)
                                linked = True # to break
                                break
                    if linked: break



                
    if linked == False:
        print("debug")
        for _ in range(len(lower_branch)):
            if lower_branch[len(lower_branch)-1-_] != cusp:
                road.append(lower_branch[len(lower_branch)-1-_])

        cusp = lower_branch[0] # NEW CUSP
        road.append(cusp) # save cusp
        print("FAIL so add at last")
        upper_branch = [cusp]
        lower_branch = [insertP, cusp] # delete points from index->end (not include index)

        linked = True # to break

    #print("Upper: ", upper_branch)
    #print("Lower: ", lower_branch)
    #print("-----------------------------------------------")
    #print("-----------------------------------------------")
    #print("-----------------------------------------------")
    if linked == False:
        print("FAIL!!!")
    return cusp, upper_branch, lower_branch
            
last_zero = None
last_state = None
timesss = 0


for diagonal in diagonals: # check diagonal one by one
    print("Current diagonal: ", diagonal)
    if diagonal == [(0.0, 3.0), (1.5, 2.0)]:#[(8.0, 5.5), (8.0, 4.5)]:#[(0.0, 3.0), (1.5, 2.0)]:#[(5.5, 4.5), (5.0, 5.5)]:#[(1.5, 1.5), (5.0, 0.0)]:  #
        print("debug")
    if timesss == 0: # initial case
            global_upper_branch.insert(0, diagonal[0])
            global_lower_branch.insert(0, diagonal[1])
            timesss += 1

    # check which branch has reach the diagonal (the upper)
    elif diagonal[0] == global_upper_branch[0] or diagonal[1] == global_upper_branch[0]:
        if diagonal[0] == global_upper_branch[0]:
            insertP = diagonal[1]
        else: insertP = diagonal[0]

        cusp, global_lower_branch, global_upper_branch = general_step(insertP, diagonal, cusp, global_lower_branch, global_upper_branch)

    elif diagonal[0] == global_lower_branch[0] or diagonal[1] == global_lower_branch[0]: # update upper
        if diagonal[0] == global_lower_branch[0]:
            insertP = diagonal[1]
        else: insertP = diagonal[0]

        cusp, global_upper_branch, global_lower_branch = general_step(insertP, diagonal, cusp, global_upper_branch, global_lower_branch)
    else: # case only contain cusp or FAIL:
        if len(global_upper_branch) == 1 and len(global_lower_branch) == 1: # ensure not FAIL
            global_upper_branch.insert(0, diagonal[0])
            global_lower_branch.insert(0, diagonal[1])

        else:
            print("yowaimushi")

    plotTriangulate(upper=global_upper_branch, lower=global_lower_branch, road=road, count=count)
    count += 1






# final step:

# ==============================================
#              FINAL STEP
# ==============================================



last_diag = [insertP, destination]
print("Current diagonal: ", last_diag)
if last_diag == [(8.0, 5.5), (8.0, 4.5)]:#[(0.0, 3.0), (1.5, 2.0)]:#[(5.5, 4.5), (5.0, 5.5)]:#[(1.5, 1.5), (5.0, 0.0)]:  #
    print("debug")

# check which branch has reach the diagonal (the upper)
if last_diag[0] == global_upper_branch[0] or last_diag[1] == global_upper_branch[0]:
    if last_diag[0] == global_upper_branch[0]:
        insertP = last_diag[1]
    else: insertP = last_diag[0]

    cusp, global_lower_branch, global_upper_branch = general_step(insertP, last_diag, cusp, global_lower_branch, global_upper_branch)

elif last_diag[0] == global_lower_branch[0] or last_diag[1] == global_lower_branch[0]: # update upper
    if last_diag[0] == global_lower_branch[0]:
        insertP = last_diag[1]
    else: insertP = last_diag[0]

    cusp, global_upper_branch, global_lower_branch = general_step(insertP, last_diag, cusp, global_upper_branch, global_lower_branch)
else: # case only contain cusp or FAIL:
    if len(global_upper_branch) == 1 and len(global_lower_branch) == 1: # ensure not FAIL
        global_upper_branch.insert(0, last_diag[0])
        global_lower_branch.insert(0, last_diag[1])

    else:
        print("yowaimushi")

plotTriangulate(upper=global_upper_branch, lower=global_lower_branch, road=road, count=count)
count += 1



def final(branch):
    for _ in reversed(branch):
        if _ not in road:
            road.append(_)
ok = False
for _ in global_upper_branch:
    if destination == _:
        final(global_upper_branch)
        ok = True
        break
if not ok:     
    for _ in global_lower_branch:
        if destination == _:
            final(global_lower_branch)
            break


#road.append()
print("road: ", road)
lastplot(road, count)

print("---------EXIT-----------")
print("Finding Shortest path and exit successfully")


