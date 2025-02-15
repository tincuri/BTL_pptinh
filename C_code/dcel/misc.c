#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "dcel.h"
#include "misc.h"

int vertex_count = 0;
struct dcel_vertex *first;
struct dcel_edge *f_edge;

int read_polygon_file(char *filename);
void test(void);

/*           uncomment to check           */
/*int main(int argc, char *argv[])*/
/*{*/
/*  if (argv[1] == NULL) {*/
/*    printf("Please input the polygon file\n");*/
/*    return -1;*/
/*  }*/
/*  read_polygon_file(argv[1]);*/
/*  printf("vertex count %d\n", vertex_count);*/
/*  test();*/
/*  return EXIT_SUCCESS;*/
/*}*/

/* read the polygon file and make it */
int read_polygon_file(char *filename){
  FILE *infile;/* pointer to the file */
  double x, y;
  struct dcel_vertex *one, *two, *second;
  struct dcel_edge *edge1, *edge2, *l_edge;
  struct dcel_face *face;

  /* read the file */
  if ((infile = fopen(filename, "r")) == NULL) {
    perror(filename);
    return -1;
  } /* error checking */
  
  /* make the first edge */
  fscanf(infile, "%lf, %lf", &x, &y);
    vertex_count++;
  first = new_vertex(x, y);
  fscanf(infile, "%lf, %lf", &x, &y);
    vertex_count++;
  second = new_vertex(x, y);
  one = second;

  edge1 = new_edge(first, second);
  f_edge = edge1;
  /* make the edges */
  do {
  if(fscanf(infile, "%lf, %lf,", &x, &y) > 0) {
      two = new_vertex(x, y);
      edge2 = new_edge(one, two);  
      next_prev(edge1, edge2);
      edge1 = edge2;
      one = two;
      vertex_count++;
    };
  } while (fgetc(infile) != EOF);
  l_edge = new_edge(one, first); /* last edge */
  next_prev(edge2, l_edge);
  next_prev(l_edge, f_edge);

  /* point all the face of the twin edge to be outside */
  edge1 = l_edge;

  do {
    edge1 = edge1->Next;
    face = malloc(sizeof(struct dcel_face));
    face->Inside = false;
    edge1->Twin->IncidentFace = face;
  } while (edge1 != l_edge);

  return vertex_count;

}

/* just a function to test */
void test(void){
  double iti, ni, san, yon;
  struct dcel_edge *one, *two, *three, *four, *five, *six;
  one = f_edge;
  two = f_edge->Next;
  three = two->Next;
  four = three->Next;
  five = four->Next;


}
/*int read_segment_file(char *filename, int *genus);*/
