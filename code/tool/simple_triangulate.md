# AN $O(n log log n)$-TIME ALGORITHM FOR TRIANGULATING A SIMPLE POLYGON

ROBERT E. TARJAN AND CHRISTOPHER J. VAN WYK

## Abstract.

Given a simple $n$-vertex polygon, the triangulation problem is to partition the interior of the polygon into $n-2$ triangles by adding $n-3$ nonintersecting diagonals.

- proposing an $O(n log logn)$-time algorithm
- improving on the previously best bound of $O (n log n)$ (?)
- showing that triangulation is not as hard as sorting. (?)
- Improved algorithms for testing whether a polygon is simple

## Introduction

Let $P$ be an $n$-vertex simple polygon, defined by a list $v_0, v_1,... v_(n-1)$ of its vertices in clockwise order around the boundary (lgh: current ccw). 

Denote the boundary of $P$ by $δP$.

**Assume throughout this  paper**: vertices of $P$ have distinct $y$-coordinates (lgh: maybe). For convenience $v_n = v_0$

## Goal 

*To find $n-3$ nonintersecting diagonals of $P$*

If $P$ is convex, any pair of vertices defines a diagonal $\rightarrow$ triangulate $P$ in $O ( n )$ time.

If $P$ is not convex, not all pairs of vertices define diagonals, and even finding one diagonal, let alone triangulating $P$, is not a trivial problem.

## History

- In 1978, Garey, Johnson, Preparata and Tarjan presented an $O (n log n)$-time.
- Some work on linear-time.
- Some work on $O(n log k)$ and worst case is $(n log n)$.
  
*In this paper we propose an $O (n log logn)$-time triangulation algorithm, thereby showing that triangulation is indeed easier than sorting.*

Reduction of the triangulation problem to the problem of computing visibility information along a single direction, which we take to be horizontal (lgh: that's why they needed distinct $y$-coordinates)

- *vertex-edge visible pair*: a vertex and an edge that can be connected by an open horizontal line segment that lies entirely inside $P$.
- *edge-edge visible pair*: a pair of edges that can be connected by an open horizontal line segment that lies entirely inside $P$.
- Linear-time equivalent to computing all vertex-edge visible pairs (lgh: ?)

*What we shall actually produce is an $O (n log log n)$ -time algorithm for computing visible pairs, which by this reduction leads to an $O (n log log n)$-time triangulation algorithm.* (lgh: ?)

Our visibility algorithm computes not only vertex-edge visible pairs but also possibly some edge-edge visible pairs. It is reassuring that the total number of visible pairs of either kind is linear.

**LEMMA 1**. *There are at most $2n$ vertex-edge visible pairs and at most $2n$ edge-edge visible pairs.*

The second cornerstone of our method is the intimate connection between visibility computation and the Jordan sorting problem.

For a simple polygon $P$ and a horizontal line $L$, the Jordan sorting problem is to sort the intersection points of $δP$ and $L$ by $x$-coordinate, given as input *only a list of the intersections in the order in* which they occur clockwise around $δP$. (The list of vertices of $P$ is *not* part of the input.)

**LEMMA 2**. *Using an algorithm to compute vertex-edge visible pairs, one can solve the Jordan sorting problem for an n-vertex polygon $P$ in $O (n)$ additional time, given as input the polygon and the line $L$ (and not the intersections).* (LGH: ?)

Since any visibility computation does Jordan sorting implicitly, it is natural to try using Jordan sorting explicitly to compute visible pairs, leads to divide-and-conquer visibility algorithm:

- Step 1: Given $P$, choose a vertex $v$ of $P$ that does not have maximum or minimum $y$-coordinate.
  - If no such $v$ exists, stop: there are no visible pairs to compute.
  - Else, let $L$ be the horizontal line through $v$.
- Step 2: Determine the intersection points of $δP$ and $L$ in the order in which they occur along the boundary of $P$. Hardest: to avoid quadratic time:
  - First, it is possible for the algorithm to report redundant visibility pairs. We call this augmented sorting method *Jordan sorting with error-correction*.
  - Second, actually finding the intersections to beat the $O (n log n)$ time bound of previous triangulation algorithms, we need another idea, that of *balanced divide and conquer*. 
- Step 3: Jordan sort the intersection points and report the visible pairs that correspond to consecutive intersection points along $L$.
- Step 4: Slice $P$ along $L$, dividing $P$ into a collection of subpolygons. (LGH: need to update insert, delete vertex method in class Polygon)
- Step 5: Apply the algorithm recursively to each subpolygon computed in Step 4.