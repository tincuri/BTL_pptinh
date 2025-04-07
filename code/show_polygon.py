import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from tool.polygon import Polygon # type: ignore
from tool.point import Point # type: ignore

# ============================================================================================
#              This file takes C output sleeve (already has simple polygon) => Lee alg
# ============================================================================================



# ==============================================
#              PATH
# ==============================================
nn = [200, 400, 600, 1000, 1200, 1400, 1600, 1800, 2000,2200, 2400]
for n in nn:
    simplePolygonPath = f"dataset/Cinput/c_case_{n}.txt"
    sleevePath = "./dataset/Coutput/maze_sleeve.txt"
    
    # code/figure/lee/{yourname}/example_{count}.png  make sure create the {yourname} folder in code/figure/lee
    savefigPath ="./figure/lee/example_0/"
    
    
    
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
    
    
    aqaq = np.array([[_.coor()[0], _.coor()[1]] for _ in polygon.vertices])
    x_in = aqaq[:, 0]
    y_in = aqaq[:, 1]
    
    # plot
    arr = polygon.getNew_array()
    arr = np.vstack((arr, arr[0]))
    # plt.scatter(x_in, y_in, marker='o')  # Create the scatter plot
    plt.plot(arr[:, 0], arr[:, 1], 'r--', lw=2)
    #plt.savefig(savefigPath+"example.png")
    plt.title(label= f"{n}")
    plt.show() # show origin simple polygon
    
