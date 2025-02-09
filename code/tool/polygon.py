import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
import sys
from typing import Union
from point import Point # type: ignore
from line import Segment, Line, Ray

import heapq


class Polygon:
    """Represents a polygon defined by a list of vertices.

    Attributes:
        vertices (list): List of Point objects representing the polygon's vertices (clockwise order).
        edges (list): List of Segment objects representing the polygon's edges.
        new_array (numpy.ndarray): Array of vertex coordinates.

    Methods:
        __init__(self, vertices): Initializes a Polygon object.
        getNew_array(self) -> numpy.ndarray: Returns an array of vertex coordinates.
        intersect(self, query_edge: 'Segment') -> bool: Checks if the polygon intersects a given Segment.
        canInsert(self, point: 'Point', seg: 'Segment') -> bool: Checks if a point can be inserted between two points of a segment without intersections.
        __str__(self) -> str: Returns a string representation of the Polygon (currently empty).
    """
    # polygon is constructed from a list of vertices (in cw order)
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = [Segment(vertices[i], vertices[i+1]) for i in range(len(vertices)-1)] + [Segment(vertices[-1], vertices[0])]
        """
        # edges are found and added as a parameter (type list)
        edges = []
        for i in range(len(vertices)-1):
            # debug
            # print("len vertices = ", len(vertices))
            # print("2 vertices = ", vertices[i], vertices[i+1], type(vertices[i]))
            e = Segment(vertices[i], vertices[i+1])
            edges.append(e)
        edges.append(Segment(vertices[-1], vertices[0]))
        self.edges = edges"""

        self.getNew_array()

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
    
    def __str__(self):
        pass

def ok(): # for debug
    pass

def old_SimplePolygon(polygon: 'Polygon', set: 'list', pos_vertices: 'list'):
    distances = []
    heapq.heapify(distances)

    for edge in polygon.edges:
        min_distance = None
        for point in set:
            
            current_distance = edge.distance1(point)
            if min_distance == None:
                min_distance = current_distance
                sap_push = [current_distance, point, edge]
            elif current_distance < min_distance:
                min_distance = current_distance
                sap_push = [current_distance, point, edge]
        print(len(distances))
        try:
            heapq.heappush(distances, sap_push) # [(distance, point, segment)]
        except TypeError: # case min_distance of two segments are one point.
            pass
    ii = 0
    success = 0
    #for point in set:
    while set != [] and distances != []:
        #ii += 1
        #print(ii)

        #if ii == 176:
        #    ok()
        current_distance = None
        # get the current shortest distance and its corresponding edge-point pair
        try:
            current_distance = heapq.heappop(distances)
            point = current_distance[1]
            edge = current_distance[2]
        except TypeError:
            pass

        # check if the edge exists in the current polygon
        """containsE = False
        for edge in polygon.edges:
            if e.start == edge.start and e.end == edge.end:
                containsE = True"""

        # proceed only if edge is in polygon, point is in interior, and it is a 
        # valid addition to the polygon
        # point in set:
        if current_distance != None:
            inset = False
            for _ in set:
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

            print(f"current check: {point}, {edge}: {edge.p}, {edge.q}, {current_distance[0]}")
            success += 1
            if success == 3:
                print("start debug")

            set.remove(point)
            # update MinPQ by adding distances between two new edges
            # and every point in interior
            e1 = Segment(edge.p, point)
            e2 = Segment(point, edge.q)
            for _ in [e1, e2]:
                for point in set:
                    min_distance = None
                    current_distance = e1.distance1(point)
                    if min_distance == None:
                        min_distance = current_distance
                        sap_push = [current_distance, point, edge]
                    elif current_distance < min_distance:
                        min_distance = current_distance
                        sap_push = [current_distance, point, edge]
                try:
                    heapq.heappush(distances, sap_push)
                except TypeError:
                    print("TypeError")
                    pass

    return polygon, set

def SimplePolygon(polygon: 'Polygon', set: 'list', pos_vertices: 'list'):
    """Refines a polygon by iteratively adding points from a set.

    Finds the closest point in `pos_vertices` to each edge of the polygon, 
    and if it meets certain criteria (inside polygon, no intersections), adds
    it to the polygon.

    Args:
        polygon (Polygon): The polygon to refine.
        set (list): A set of points.
        pos_vertices (list): A list of potential vertices to add.

    Returns:
        tuple (Polygon, list): The refined polygon and the updated set of points.
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
            """elif current_distance < min_distance:
                min_distance = current_distance
                sap_push = [current_distance, point, edge]"""
        #print(len(distances))
        try:
            heapq.heappush(distances, sap_push) # [(distance, point, segment)]
        except TypeError: # case min_distance of two segments are one point.
            pass
    ii = 0
    success = 0
    #for point in set:
    while pos_vertices != [] and distances != []:
        #ii += 1
        #print(ii)

        #if ii == 176:
        #    ok()
        current_distance = None
        # get the current shortest distance and its corresponding edge-point pair
        try:
            current_distance = heapq.heappop(distances)
            point = current_distance[1]
            edge = current_distance[2]
        except TypeError:
            continue  # Skip if heap is empty or other type error

        # check if the edge exists in the current polygon
        """containsE = False
        for edge in polygon.edges:
            if e.start == edge.start and e.end == edge.end:
                containsE = True"""

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

            #print(f"current check: {point}, {edge}: {edge.p}, {edge.q}, {current_distance[0]}")
            #success += 1
            #if success == 3:
            #    print("start debug")

            set.remove(point)
            pos_vertices.remove(point)
            # update MinPQ by adding distances between two new edges
            # and every point in interior
            """e1 = Segment(edge.p, point)
            e2 = Segment(point, edge.q)
            for _ in [e1, e2]:
                for point in pos_vertices:
                    min_distance = None
                    current_distance = e1.distance1(point)
                    if min_distance == None:
                        min_distance = current_distance
                        sap_push = [current_distance, point, edge]
                    elif current_distance < min_distance:
                        min_distance = current_distance
                        sap_push = [current_distance, point, edge]
                try:
                    heapq.heappush(distances, sap_push)
                except TypeError:
                    print("TypeError")
                    pass"""

    return polygon, set #, pos_vertices

    
"""vertices = [Point(0, 0), Point(1, 0), Point(2,1), Point(-1, 1), Point(0, 2), Point(1, 2)]
polygon = Polygon(vertices)
d = Segment(Point(0, 3), Point(3, 0))
print(polygon.intersect(d))
"""
