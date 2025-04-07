import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from tool.polygon import Polygon # type: ignore
from tool.point import Point # type: ignore
import scipy
import time

# ==============================================
#              SUPPORTING FUNCTION
# ==============================================


# RETURN TRUE IF A->B->C CCW, FALSE IF THEY'RE NOT
def isccw_x(a, b, c):
    """Return True if A->B->C is counterclockwise."""
    return (c[1]-a[1]) * (b[0]-a[0]) > (b[1]-a[1]) * (c[0]-a[0])

# Show the origin simple polygon (for checking if it not a simple polygon)
def showOriginSP(polygon: 'Polygon'):
    global savefigPath
    aqaq = np.array([[_.coor()[0], _.coor()[1]] for _ in polygon.vertices])
    x_in = aqaq[:, 0]
    y_in = aqaq[:, 1]

    # plot
    arr = polygon.getNew_array()
    arr = np.vstack((arr, arr[0]))
    plt.scatter(x_in, y_in, marker='o')  # Create the scatter plot
    plt.plot(arr[:, 0], arr[:, 1], '#000000', lw=2)
    # plt.savefig(savefigPath+"example.png")
    plt.show()

# Plot the polygon outline
def plot_polygon_outline():
    """Plot the polygon"""
    global road
    vertex_x = [vertex[0] for vertex in vertexes]
    vertex_y = [vertex[1] for vertex in vertexes]
    plt.plot(vertex_x, vertex_y, color='#000000', linestyle='-')

    # Shortest way
    x_road = [point[0] for point in road]
    y_road = [point[1] for point in road]
    plt.scatter(x_road, y_road, marker='s', color='black')
    plt.plot(x_road, y_road, color='red')

# plot the last time ( result ) # TWO IMAGE, FIRST WITH DIAGONALS, SECOND (RESULT) WITHOUT DIAGONALS
def lastplot(count: 'int'):
    plt.clf()
    plot_polygon_outline()

    # points and diag
    x = []
    y = []
    for diag in plot_diag:
        x = [point[0] for point in diag]
        y = [point[1] for point in diag]
        plt.scatter(x, y, marker='p', color='blue')
        plt.plot(x, y, color='#000000', linestyle='--')
    # plt.savefig(savefigPath+f"example_{count}.png")
    plt.show()


    # PLOT without diag
    count += 1
    plt.clf()
    plot_polygon_outline()
    # plt.savefig(savefigPath+f"example_{count}.png")
    plt.show()

# PLOT TO INSERT TO THE REPORT
def plotTriangulate(upper: 'list', lower: 'list', count: 'int'):
    plt.clf()
    plot_polygon_outline()

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

    # plt.savefig(savefigPath+f"example_{i}_{count}.png")
    plt.show()

# 2 functions for General step in the Algorithm
def general_step(insertP: 'Point', diagonal: 'list', upper_branch: 'list', lower_branch: 'list'):
    global cusp, road
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

    # nothing added -> add to the lastest point
    if linked == False:
        #print("debug")
        for _ in range(len(lower_branch)):
            if lower_branch[len(lower_branch)-1-_] != cusp:
                road.append(lower_branch[len(lower_branch)-1-_])

        cusp = lower_branch[0] # NEW CUSP
        road.append(cusp) # save cusp
        #print("FAIL so add at last")
        upper_branch = [cusp]
        lower_branch = [insertP, cusp] # delete points from index->end (not include index)
        linked = True # to break

    #print("-----------------------------------------------")
    #print("-----------------------------------------------")
    #print("-----------------------------------------------")
    if linked == False:
        print("FAIL!!!")
    return cusp, upper_branch, lower_branch
            
def alg(diagonal: 'list'):
    global global_upper_branch, global_lower_branch, cusp, timesss, insertP # <--- declare them as global
    if timesss == 0: # initial case
            global_upper_branch.insert(0, diagonal[0])
            global_lower_branch.insert(0, diagonal[1])
            timesss += 1

    # check which branch has reach the diagonal (the upper)
    elif diagonal[0] == global_upper_branch[0] or diagonal[1] == global_upper_branch[0]:
        if diagonal[0] == global_upper_branch[0]:
            insertP = diagonal[1]
        else: insertP = diagonal[0]

        cusp, global_lower_branch, global_upper_branch = general_step(insertP, diagonal, global_lower_branch, global_upper_branch)

    elif diagonal[0] == global_lower_branch[0] or diagonal[1] == global_lower_branch[0]: # update upper
        if diagonal[0] == global_lower_branch[0]:
            insertP = diagonal[1]
        else: insertP = diagonal[0]

        cusp, global_upper_branch, global_lower_branch = general_step(insertP, diagonal, global_upper_branch, global_lower_branch)
    else: # case only contain cusp or FAIL:
        if len(global_upper_branch) == 1 and len(global_lower_branch) == 1: # ensure not FAIL
            global_upper_branch.insert(0, diagonal[0])
            global_lower_branch.insert(0, diagonal[1])

        else:
            return False



# ============================================================================================
#              This file takes C output sleeve (already has simple polygon) => Lee alg
# ============================================================================================


lee = open("../output/lee_time.txt", "w")
jikan = [] # for time recognizing

# ==============================================
#              PATH
# ==============================================

nn = np.array([200, 400, 600, 1000, 1200, 1400, 1600, 1800, 2000,2200, 2400])
for qqq in nn:
    simplePolygonPath = f"dataset/Cinput/c_case_{qqq}.txt"
    sleevePath = f"../output/triangulation/sleeve_{qqq}.txt"
    
    # code/figure/lee/{yourname}/example_{count}.png  make sure create the {yourname} folder in code/figure/lee
    savefigPath ="./figure/lee/example_data/"



    # ==============================================
    #              SIMPLE POLYGON
    # ==============================================

    # take input from C
    f = open(simplePolygonPath, "r")
    # insert input points to list
    set = [] # set of all points which hasn't become verticle
    n = int(f.readline())
    for i in range(n):
        coor = f.readline().split(' ')
        set.append(Point(coor[0], coor[1].replace('\n', ""))) # set of points 'Point'
    polygon = Polygon(set)

    # In case you want to show the origin simple polygon
    showOriginSP(polygon)



    # ==============================================
    #              SLEEVE
    # ==============================================

    f = open(sleevePath, "r")
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

    # polygon vertex (for plotting)
    vertexes = polygon.getNew_array()
    vertexes = np.vstack([vertexes, vertexes[0]]) 



    # ==============================================
    #              MAIN LOGIC BEGIN
    # ==============================================

    start = time.time()
    count = 0 # for save figure



    # ==============================================
    #              INITIAL STEP
    # ==============================================

    # Global variable
    road = [source] # list of cusp or final path
    cusp = source # LET source be the cusp
    global_upper_branch = [source]
    global_lower_branch = [source]

    up_turn = None # store the turn of two convex (can be inferenced)



    # ==============================================
    #              GENERAL STEP
    # ==============================================

    # Global variable
    timesss = 0
    insertP = diagonals[0][0] # INITIAL

    for diagonal in diagonals: # check diagonal one by one
        # print("Current diagonal: ", diagonal) # for debug
        alg(diagonal=diagonal)
        # plotTriangulate(upper=global_upper_branch, lower=global_lower_branch, count=count)
        count += 1



    # ==============================================
    #              FINAL STEP
    # ==============================================

    try:
        last_diag = [insertP, destination]
        alg(last_diag)
    except:
        insertP = diagonal[1]
        last_diag = [insertP, destination]
        if not alg(last_diag): # mean insertP == diagonal[0]
            insertP = diagonal[0]
            last_diag = [insertP, destination]
            if not alg(last_diag):
                print("yowamushi")
    # plotTriangulate(upper=global_upper_branch, lower=global_lower_branch, count=count)
    # count += 1



    def final(branch: list[tuple[float, float]]):
        for node in reversed(branch):
            if node not in road:
                road.append(node)
    if destination in global_upper_branch:
        final(global_upper_branch)
    elif destination in global_lower_branch: 
        final(global_lower_branch)

    # print("road: ", road)
    lastplot(count)
    delta = time.time() - start
    jikan.append(delta)

    lee.write(f"{qqq}, {time.time() - start}\n")
res = scipy.stats.linregress(nn, jikan)
plt.plot(nn, res.intercept + res.slope*nn)
plt.plot(nn, jikan, "ro")
plt.savefig("lee_graph.png")
plt.show()