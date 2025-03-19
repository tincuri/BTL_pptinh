#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>

#include "dcel.h"
#include "misc.h"

struct point *scan_point(FILE *pos) {
  double x, y;
  char ch;

  while (isspace(ch = fgetc(pos)))
    ;                                        // Skip whitespace
  ungetc(ch, pos);                           // Put back the non-space character
  if (fscanf(pos, "(%lf,%lf)", &x, &y) == 2) /* be sure that it work */
    return new_point(x, y);
  return NULL;
}

struct dcel_vertex *scan_vertex(FILE *pos) {
  double x, y;
  char ch;

  while (isspace(ch = fgetc(pos)))
    ;                                        // Skip whitespace
  ungetc(ch, pos);                           // Put back the non-space character
  if (fscanf(pos, "%lf %lf", &x, &y) == 2) /* be sure that it work */
    return new_vertex(x, y);
  return NULL;
}

struct dcel_edge *scan_edge(FILE *pos) {
  int x, y;
  char ch;

  while (isspace(ch = fgetc(pos)))
    ;                                      // Skip whitespace
  ungetc(ch, pos);                         // Put back the non-space character
  if (fscanf(pos, "(%d,%d)", &x, &y) == 2) /* be sure that it work */
    return new_edge(vertex_list[x], vertex_list[y]);
  return NULL;
}
