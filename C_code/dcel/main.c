#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#include "dcel.h"
#include "make_dcel.h"
#include "misc.h"
#include "scan.h"

int face1, face2; /* face index of the 2 points */
struct point *p1, *p2;/* the 2 points */

int read_point_file(char *filename);
void print_edge(struct dcel_edge *h_edge);
void write_edge(FILE *infile, struct dcel_edge *h_edge);
void write_result(void);

int main(int argc, char *argv[])
{
  struct node *t;
  if (argv[1] == NULL) {
    printf("Please input the polygon file\n");
    return -1;
  }
  if (argv[2] == NULL){
    printf("Please input the triagulated edges file\n");
    return -1;
  }
  if (argv[3] == NULL){
    printf("Please input the 2 points locations\n");
    return -1;
  }
  read_polygon_file(argv[1]);
  read_edge_file(argv[2]);
  read_point_file(argv[3]);
  create_dcel();
  face1 = point_location(p1);
  face2 = point_location(p2);
  find_sleeve();
   
  printf("These are the diagonals in the sleeve\n");
  for ( t = head->next; t != z; t = t->next) {
    print_edge(t->half_edge);
  }
  write_result();

  return EXIT_SUCCESS;
}
void print_edge(struct dcel_edge *h_edge){
  printf("(%g, %g) - (%g, %g)\n", h_edge->Origin->x, h_edge->Origin->y, h_edge->Twin->Origin->x, h_edge->Twin->Origin->y);
}
void write_edge(FILE *infile, struct dcel_edge *h_edge){
  fprintf(infile, "%g %g %g %g\n", h_edge->Origin->x, h_edge->Origin->y, h_edge->Twin->Origin->x, h_edge->Twin->Origin->y);
}
int read_point_file(char *filename){
  FILE *infile;
  char ch;
  double x, y;
  /* read the file */
  if ((infile = fopen(filename, "r")) == NULL) {
    perror(filename);
    return -1;
  } /* error checking */

  /* do it twice for the 2 points */
  while (isspace(ch = fgetc(infile)));  // Skip whitespace
  ungetc(ch, infile);      // Put back the non-space character
  if (fscanf(infile, "(%lf,%lf)", &x, &y) == 2) /* be sure that it work */
  p2 = new_point(x, y);

  while (isspace(ch = fgetc(infile)));  // Skip whitespace
  ungetc(ch, infile);      // Put back the non-space character
  if (fscanf(infile, "(%lf,%lf)", &x, &y) == 2) /* be sure that it work */
  p1 = new_point(x, y);
}

void write_result(void){
  FILE *infile;
  struct node *t;

  infile = fopen("sleeve.txt", "w");
  for ( t = head->next; t != z; t = t->next) {
    write_edge(infile, t->half_edge);
  }
}
