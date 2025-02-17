#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#include "dcel.h"

struct dcel_vertex *scan_point(FILE *pos){
  double x, y;
  char ch;

  while (isspace(ch = fgetc(pos)));  // Skip whitespace
  ungetc(ch, pos);      // Put back the non-space character
  if (fscanf(pos, "(%lf,%lf)", &x, &y) == 2) /* be sure that it work */
  return new_vertex(x, y);
}

struct dcel_edge *scan_edge(FILE *pos){
  int x, y;
  char ch;

  while (isspace(ch = fgetc(pos)));  // Skip whitespace
  ungetc(ch, pos);      // Put back the non-space character
  if (fscanf(pos, "(%d,%d)", &x, &y) == 2) /* be sure that it work */
  return new_edge(vertex_list[x], vertex_list[y]);
}


