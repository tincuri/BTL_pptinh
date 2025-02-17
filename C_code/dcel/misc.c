#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "dcel.h"

double angle(struct dcel_edge *edge1, struct dcel_edge *edge2){
  double x1, x2, x3, y1, y2, y3;
  double a1, a2, b1, b2;
  double length1, length2, crossProduct, sin, dotProduct, angle;
  edge1->Origin->x = x1;
  edge1->Twin->Origin->x = x2;
  edge2->Twin->Origin->x = x3;
  edge1->Origin->y = y1;
  edge1->Twin->Origin->y = y2;
  edge2->Twin->Origin->y = y3;

  a1 = (x2 - x1);
  a2 = (y2 - y1);
  b1 = (x3 - x1);
  b2 = (y3 - y1);
  /**/
  /*length1 = pow((pow(a1, 2) + pow(a2, 2)), 0.5); */
  /*length2 = pow((pow(b1, 2) + pow(b2, 2)), 0.5); */
  /*crossProduct = a1b2 - a2b1;*/
  /*dotProduct = a1b1 + a2b2;*/
  /*sin = crossProduct / (length1 * length2);*/
  /*cos = dotProduct / (length1 * length2);*/
  /**/

  angle = atan2(b1, b2) - atan2(a1, a2);

  return angle;
}

void sort_edge(struct dcel_edge **list_edge){
  printf("temp\n");
}

/* TODO: implement insertionsort and mergesort */

