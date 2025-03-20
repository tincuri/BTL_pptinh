#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "dcel.h"
#include "make_dcel.h"
#include "misc.h"
#include "scan.h"
#include "../seidel-1.0/triangulate.h"
#include "../find_edge/find_edge.h"

int face1, face2;      /* face index of the 2 points */
struct point *p1, *p2; /* the 2 points */
double **vertex_array; /* array of vertex as x and y */
int **triangles; /* array of 2 index of a triangle */


int read_point_file(char *filename); /* make the 2 points */
void print_edge(struct dcel_edge *h_edge); /* print an edge to screen */
void write_edge(FILE *infile, struct dcel_edge *h_edge); /* write edge to output */
void write_result(char *output); /* write result to output */
void reprocess(int op[SEGSIZE][3], int ntriangles); /*make the index 0th again (because the lib didnt do so) */

int main(int argc, char *argv[]) {
  struct node *t;
  if (argc < 4) {
    fprintf(stderr, "ERROR: Missing some files\n");
    fprintf(stderr, "USAGE: ./sleeve <polygon_file> <2_points_locations> <output>\n");
    exit(EXIT_FAILURE);
  }

  if(read_polygon_file(argv[1]) < 0)
    exit(EXIT_FAILURE);

  int op[vertex_count][3], ntriangles;

  ntriangles = triangulate_from_file(op, argv[1]); /* function from the lib */
  reprocess(op, ntriangles);
  get_edges(op, ntriangles);
  edge_from_graph(edge_graph);
  /*read_edge_file(argv[2]);*/
  if(read_point_file(argv[2]) < 0)
    exit(EXIT_FAILURE);
  create_dcel();


  face1 = point_location(p1);
  face2 = point_location(p2);
  find_sleeve();

  printf("These are the diagonals in the sleeve\n");
  for (t = head->next; t != z; t = t->next) {
    print_edge(t->half_edge);
  }
  printf("\n");
  write_result(argv[3]);

  return EXIT_SUCCESS;
}

void init_triangles(void){
  triangles = malloc(vertex_count * sizeof(int *));
  for (int i = 0; i < vertex_count; i++)
    triangles[i] = malloc(3 * sizeof(int));
}
void create_vertex_array(void){
  /* init the array */
  vertex_array = malloc((vertex_count + 1) * sizeof(int *)); /* the lib require start at 1 */
  for (int j = 0; j < vertex_count + 1; j++)
    vertex_array[j] = malloc(2 * sizeof(double));

  for (int i = 0; i < vertex_count; i++) {
    vertex_array[i+1][0] = vertex_list[i]->x;
    vertex_array[i+1][1] = vertex_list[i]->y;
  }
}

void print_edge(struct dcel_edge *h_edge) {
  printf("(%g, %g) - (%g, %g)\n", h_edge->Origin->x, h_edge->Origin->y,
         h_edge->Twin->Origin->x, h_edge->Twin->Origin->y);
}

void write_edge(FILE *infile, struct dcel_edge *h_edge) {
  fprintf(infile, "%g %g %g %g\n", h_edge->Origin->x, h_edge->Origin->y,
          h_edge->Twin->Origin->x, h_edge->Twin->Origin->y);
}

int read_point_file(char *filename) {
  FILE *infile;
  char ch;
  double x, y;
  /* read the file */
  if ((infile = fopen(filename, "r")) == NULL) {
    perror(filename);
    return -1;
  } /* error checking */

  /* do it twice for the 2 points */
  while (isspace(ch = fgetc(infile)))
    ;                 // Skip whitespace
  ungetc(ch, infile); // Put back the non-space character
  if (fscanf(infile, "(%lf,%lf)", &x, &y) == 2) /* be sure that it work */
    p2 = new_point(x, y);

  while (isspace(ch = fgetc(infile)))
    ;                 // Skip whitespace
  ungetc(ch, infile); // Put back the non-space character
  if (fscanf(infile, "(%lf,%lf)", &x, &y) == 2) /* be sure that it work */
    p1 = new_point(x, y);
  return 0;
}

void write_result(char *output) {
  FILE *infile;
  struct node *t;

  infile = fopen(output, "w");
  for (t = head->next; t != z; t = t->next) {
    write_edge(infile, t->half_edge);
  }
  printf("Finished writing result to <%s>\n", output);
}

void reprocess(int op[SEGSIZE][3], int ntriangles){
  for (int i = 0; i < ntriangles; i++){
    --op[i][0];
    --op[i][1];
    --op[i][2];
  }
}
