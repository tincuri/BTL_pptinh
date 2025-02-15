import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
import sys
from typing import Union
from point import Point # type: ignore
from line import Segment, Line, Ray
import math

import heapq


class Polygon:
    """Represents a polygon defined by a list of vertices.

    Attributes:
        vertices (list of Point): Polygon vertices in clockwise order.
        edges (list of Segment): Polygon edges.
        new_array (numpy.ndarray): Vertex coordinates.

    Methods:
        __init__(vertices): Initializes the polygon.
        getNew_array() -> numpy.ndarray: Returns vertex coordinates.
        intersect(query_edge: 'Segment') -> bool: Checks for intersection.
        canInsert(point: 'Point', seg: 'Segment') -> bool: Validates point insertion.
        verticesType() -> list: Classifies vertices.
        newangle(p1: 'Point', p2: 'Point', p3: 'Point') -> float: Computes the angle.
        __str__() -> str: Returns string representation.
    """
    # polygon is constructed from a list of vertices (in cw order)
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = [Segment(vertices[i], vertices[i+1]) for i in range(len(vertices)-1)] + [Segment(vertices[-1], vertices[0])]
        self.getNew_array() # update new_array

    def getNew_array(self):
        self.new_array = np.ndarray(shape=(len(self.vertices), 2), dtype=float)
        self.new_array[:] = [[float(_.coor()[0]), float(_.coor()[1])] for _ in self.vertices]
        return self.new_array

    # checks whether polygon intersects with a query edge
    def intersect(self, query_edge):
        for edge in self.edges:
            # if the query edge and polygon edge don't share a vertex
            if edge.p != query_edge.p and edge.q != query_edge.q and edge.q != query_edge.p and edge.q != query_edge.p:
                # return true if polygon edge intersects with query edge
                if edge.intersect(query_edge):
                    return True
        return False

    def canInsert(self, point, seg: 'Segment'):
        newseg1 = Segment(seg.p, point)
        newseg2 = Segment(point, seg.q)

        for edge in self.edges:
            if (newseg1.intersect(edge) == True) or (newseg2.intersect(edge) == True):
                return False
        return True
    
    def verticesType(self):
        self.complex_vertices = []
        for i in range(len(self.vertices)):
            truoc = self.vertices[i-1]
            hientai = self.vertices[i]
            try:
                sau = self.vertices[i+1]
            except IndexError: # handle the last case
                sau = self.vertices[0]

            angle = self.newangle(truoc, hientai, sau)
            if angle < math.pi:
                if hientai.y > truoc.y and hientai.y > truoc.y:
                    queue = [hientai, "start"]
                elif hientai.y < truoc.y and hientai.y < sau.y:
                    queue = [hientai, "end"]
                else:
                    queue = [hientai, "regular"]
            elif angle > math.pi:
                if hientai.y > truoc.y and hientai.y > truoc.y:
                    queue = [hientai, "split"]
                elif hientai.y < truoc.y and hientai.y < sau.y:
                    queue = [hientai, "merge"]
                else:
                    queue = [hientai, "regular"]
            else:
                queue = [hientai, "regular"]
            self.complex_vertices.append(queue)
        return self.complex_vertices
    
    def newangle(self, p1: 'Point', p2: 'Point', p3: 'Point') -> float: # should be able to return angle from three points clock-wise
        # still wrong, only export split/merge -> angle > pi? # fixed by changed degree to rad
        # angle:   p1 --cw--> p2 --cw--> p3
        vt12 = np.array([p1.coor()[0] - p2.coor()[0], p1.coor()[1] - p2.coor()[1]])
        vt23 = np.array([p3.coor()[0] - p2.coor()[0], p3.coor()[1] - p2.coor()[1]])
        if np.all(vt12 == 0) or np.all(vt23 == 0): # handle zero vectors
            return 0 

        dot_product = np.dot(vt12, vt23)
        norm_v1 = np.linalg.norm(vt12)
        norm_v2 = np.linalg.norm(vt23)

        if norm_v1 == 0 or norm_v2 == 0:
            return 0

        cos_theta = dot_product / (norm_v1 * norm_v2)
        theta_rad = math.acos(cos_theta)

        cross_product_z = vt12[0] * vt23[1] - vt12[1] * vt23[0]

        if cross_product_z < 0:  # v2 is clockwise from v1
            angle_deg = theta_rad
        else:  # v2 is counter-clockwise from v1 or vectors are collinear
            angle_deg = 2*math.pi - theta_rad

        return angle_deg

    
    def __str__(self):
        pass

def SimplePolygon(polygon: 'Polygon', set: 'list', pos_vertices: 'list') -> tuple['Polygon', list]:
    """Refines a polygon by iteratively adding valid points.

    Finds the closest point in `pos_vertices` to each edge, ensuring it is inside 
    the polygon and does not cause intersections before insertion.

    Args:
        polygon (Polygon): The polygon to refine.
        set (list): Available points for insertion.
        pos_vertices (list): Candidate vertices for refinement.

    Returns:
        tuple (Polygon, list): The updated polygon and remaining points.
    """
    distances = []
    heapq.heapify(distances)

    for edge in polygon.edges:
        min_distance = None
        for point in pos_vertices:
            
            current_distance = edge.distance1(point)
            if min_distance == None or current_distance < min_distance:
                min_distance = current_distance
                sap_push = [current_distance, point, edge]
        try:
            heapq.heappush(distances, sap_push) # [(distance, point, segment)]
        except TypeError: # case min_distance of two segments are one point.
            pass

    while pos_vertices != [] and distances != []:

        current_distance = None
        # get the current shortest distance and its corresponding edge-point pair
        try:
            current_distance = heapq.heappop(distances)
            point = current_distance[1]
            edge = current_distance[2]
        except TypeError:
            continue  # Skip if heap is empty or other type error

        # check if the edge exists in the current polygon

        # proceed only if edge is in polygon, point is in interior, and it is a valid addition to the polygon
        # point in set:
        if current_distance != None: # for debug
            inset = False
            for _ in pos_vertices:
                if point == _:
                    inset = True
        else: inset = False 

        if inset == True and  polygon.canInsert(point, edge):
            # get index of the edge
            for poly_edge in polygon.edges:
                if edge.p == poly_edge.p and edge.q == poly_edge.q:
                    i = polygon.edges.index(poly_edge)

            # insert new edges and point into the polygon,
            # remove old edge from polygon and remove point from interior
            polygon.vertices.insert(i + 1, point) # index 0->n-1, insert 1->n
            polygon.edges[i] = Segment(edge.p, point)
            polygon.edges.insert(i + 1, Segment(point, edge.q))

            set.remove(point)
            pos_vertices.remove(point)

    return polygon, set #, pos_vertices

def lastPoint(polygon: 'Polygon', set: 'list') -> tuple['Polygon', list]:
    """Inserts the last valid point into the polygon.

    Finds the closest point in `set` to an edge, checks if it can be inserted, 
    and updates the polygon structure accordingly.

    Args:
        polygon (Polygon): The polygon to modify.
        set (list): Remaining points to consider.

    Returns:
        tuple (Polygon, list): The updated polygon and remaining points.
    """
    # the code is iterated so i need to create new function?
    for point in set:
        sap_push = None
        min_distance = None
        for edge in polygon.edges:
            current_distance = edge.distance1(point)
            if min_distance == None or current_distance < min_distance:
                min_distance = current_distance
                sap_push = [current_distance, point, edge, polygon.edges.index(edge)]

        if polygon.canInsert(sap_push[1], sap_push[2]):
            i = sap_push[3]
            polygon.vertices.insert(i + 1, point) # index 0->n-1, insert 1->n
            polygon.edges[i] = Segment(edge.p, point)
            polygon.edges.insert(i + 1, Segment(point, edge.q))
            #print(point) # for debug
        set.remove(point)
    return polygon, set
