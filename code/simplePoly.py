# -----------------------------------------------------------------------------
#   Improved polygon generation algorithm
# -----------------------------------------------------------------------------

from randomSimplePolygon.src.Edge import Edge
from randomSimplePolygon.src.Polygon import Polygon
from randomSimplePolygon.src.Math import quickhull, pnt2line


import heapq
import matplotlib.pyplot as plt
import time


if __name__ == "__main__":

    # take input from test.txt
    nn = [200, 400, 600, 1000, 1200, 1400, 1600, 1800, 2000,2200, 2400]
    for n in nn:
        # take list of vertices to make simple polygon
        f = open(f"dataset/vertices/case_{n}.txt", "r")

        # start timer
        start = time.time()

        # insert input points to list
        points = []
        n = int(f.readline())
        for i in range(n):
            coord = f.readline().split(' ')
            points.append([float(coord[0]), float(coord[1])])

        # initialize the polygon as a convex hull of the points
        polygon = Polygon(quickhull(points))

        # update points set to exclude polygon vertices
        points = [x for x in points if x not in polygon.vertices]

        # initialize MinPQ, dictionary
        distances = []
        heapq.heapify(distances)
        distancesDict = {}

        # pre-process by adding the distances between every edge-point pair into MinPQ and dictionary
        for edge in polygon.edges:
            for point in points:
                curr_dist = pnt2line(point, edge.start, edge.end)
                heapq.heappush(distances, curr_dist)
                distancesDict[curr_dist] = (edge, point)

        # iterate so long as there still exist points in the interior
        while points and len(distances) != 0:

            # get the current shortest distance and its corresponding edge-point pair
            curr_dist = heapq.heappop(distances)
            e = distancesDict[curr_dist][0]
            point = distancesDict[curr_dist][1]

            # check if the edge exists in the current polygon
            containsE = False
            for edge in polygon.edges:
                if e.start == edge.start and e.end == edge.end:
                    containsE = True

            # proceed only if edge is in polygon, point is in interior, and it is a 
            # valid addition to the polygon
            if containsE and point in points and e.valid(polygon, point):
                # get index of the edge
                for edge in polygon.edges:
                    if e.start == edge.start and e.end == edge.end:
                        i = polygon.edges.index(edge)
                # insert new edges and point into the polygon,
                # remove old edge from polygon and remove point from interior
                polygon.vertices.insert(i + 1, point)
                polygon.edges[i] = Edge(e.start, point)
                polygon.edges.insert(i + 1, Edge(point, e.end))
                points.remove(point)
                # update MinPQ by adding distances between two new edges
                # and every point in interior
                e1 = Edge(e.start, point)
                e2 = Edge(point, e.end)
                for point in points:
                    curr_dist_e1 = pnt2line(point, e1.start, e1.end)
                    curr_dist_e2 = pnt2line(point, e2.start, e2.end)
                    heapq.heappush(distances, curr_dist_e1)
                    heapq.heappush(distances, curr_dist_e2)
                    distancesDict[curr_dist_e1] = (e1, point)
                    distancesDict[curr_dist_e2] = (e2, point)

        # print results
        print()
        print("--------------- Improved Approach --------------")
        print("Number of vertices:  %i" % n)
        print("Execution time:      %s seconds" % (time.time() - start))
        print("------------------------------------------------")
        print()

        # plot the polygon
        pset = polygon.vertices
        
        # output for C code:
        f = open(f"dataset/Cinput/c_case_{n}.txt", "w")
        f.write(str(n))
        f.write("\n")
        for pp in range(len(pset)):
            px, py = pset[len(pset) - pp - 1]
            xau = str(px) + " " + str(py)
            f.write(xau)
            f.write("\n")
        f.close()

        pset.append(pset[0])

        xs, ys = zip(*pset)
        #print(xs, ys)
        plt.plot(xs, ys)
        #plt.savefig(f"code\figure\simplePolygonFig\case_{n}.png")
        # plt.show()

        # close test.txt file
        f.close()
