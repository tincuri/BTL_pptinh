import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from point import Point, midPoint # type: ignore
from line import Line, Segment, Ray # type: ignore
from construct import perpendicular, perp_bisector, parallel, angleBisector # type: ignore
from circles import Circle # type: ignore
import sys
from typing import Union
import heapq
from polygon import Polygon, SimplePolygon # type: ignore
from scipy.spatial import ConvexHull, convex_hull_plot_2d # type: ignore

def triangulate(polygon: 'Polygon', array_for_hull):
    num_diagonal = len(polygon.edges) - 2
    # start = polygon.vertices[0]
    # end = polygon.vertices[1]
    y_coor_list = [{"Point": vertex, "y_coor": float(vertex.y)} for vertex in polygon.vertices]
    sorted_y_coor_list = sorted(y_coor_list, key=lambda item: item["y_coor"])
    #print(sorted_y_coor_list)

    # STEP 1:
    if len(y_coor_list) <= 2:
        print("There are no visible pairs to compute.")
        return 0
    
    cur_point = y_coor_list[1].get("Point")
    d = Line([0, 1, -cur_point.y])

    # STEP 2:
    ### wrong way
    list_intersects = []
    for edge in polygon.edges:
        x_intersect = (d.lineVec[1]*edge.lineVec[2] - d.lineVec[2]*edge.lineVec[1]) / (d.lineVec[1] - edge.lineVec[1])
        y_intersect = (d.lineVec[2] - edge.lineVec[2]) / (edge.lineVec[1] - d.lineVec[1])
        point_intersect = Point(x_intersect, y_intersect)
        #if edge.onSegment(point_intersect):
        list_intersects.append(point_intersect)

    ### Find method to print out to check, maybe print in demo

    return list_intersects

"""
    x+By+C=0 -> line [A, B, C]
    Segment: x+by+c=0
    y = (c - C) / (B - b)
    x = (bC - Bc) / (B - b)

"""