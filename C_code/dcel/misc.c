#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <ctype.h>

#include "dcel.h"
#include "misc.h"

/*        TODO: make a scan_point function to read the file             */

int vertex_count = 0;
struct dcel_vertex *first; /* first vertex */
struct dcel_edge *f_edge; /* first edge */

void test(void);

/*           uncomment to check           */
int main(int argc, char *argv[])
{
  if (argv[1] == NULL) {
    printf("Please input the polygon file\n");
    return -1;
  }
  if (argv[2] == NULL) {
    printf("Please input the triangle file\n");
    return -1;
  }
  read_polygon_file(argv[1]);
  read_triangle_file(argv[2]);
  printf("vertex count %d\n", vertex_count);
  /*test();*/
  return EXIT_SUCCESS;
}

/* read the polygon file and make it */
int read_polygon_file(char *filename){
  FILE *infile;/* pointer to the file */
  double x, y;
  char ch;
  struct dcel_vertex *one, *two, *second;
  struct dcel_edge *edge1, *edge2, *l_edge;
  struct dcel_face *face1, *face2;

  /* read the file */
  if ((infile = fopen(filename, "r")) == NULL) {
    perror(filename);
    return -1;
  } /* error checking */
  
  /* make the first edge */
  first = scan_point(infile);
  second = scan_point(infile);
  printf("(%g, %g) | \n", first->x, first->y);
  printf("(%g, %g) | \n", second->x, second->y);
  one = second;
  vertex_count += 2; /* for the 2 vertex needed for the 1st edge */

  edge1 = new_edge(first, second);
  f_edge = edge1;
  /* make the edges */
  /*do {*/
  /*if(fscanf(infile, "(%lf, %lf)", &x, &y) > 0) {*/
  /*    two = new_vertex(x, y);*/
  /*    edge2 = new_edge(one, two);  */
  /*    next_prev(edge1, edge2);*/
  /*    edge1 = edge2;*/
  /*    one = two;*/
  /*    vertex_count++;*/
  /*    printf("(%g, %g) | \n", x, y);*/
  /*  };*/
  /*} while (fgetc(infile) != EOF);*/

while ((ch = fgetc(infile)) != '\n') { /*stop at each line */
      if (ch == '\r') { /* combat with the CRLF nonsense */
        fgetc(infile);
        break;
      }
      /*printf("%d\n", ch);*/
      ungetc(ch, infile);

      two = scan_point(infile);
      edge2 = new_edge(one, two);  
      next_prev(edge1, edge2);
      edge1 = edge2;
      one = two;
      vertex_count++;
      printf("(%g, %g) | \n", two->x, two->y);
    }

  l_edge = new_edge(one, first); /* last edge */
  next_prev(edge2, l_edge);
  next_prev(l_edge, f_edge);

  /*      add the first 2 face       */
  /* the 2 starting face */
  face1 = malloc(sizeof(struct dcel_face));
  face2 = malloc(sizeof(struct dcel_face));
  face1->type = POLYGON;
  face2->type = POLYGON;
  edge1 = l_edge;

 do { /* make it loop once */
    edge1 = edge1->Next;
    edge1->IncidentFace = face1;
    edge1->Twin->IncidentFace = face2;
  } while (edge1 != l_edge);

  return vertex_count;

}

int read_triangle_file(char *filename){

  FILE *infile;
  struct dcel_vertex *points[3], *try; /* list of 3 points */
  char ch;
  int count = 0;
  struct dcel_edge *test;
  struct dcel_face *play;

  /* read the file */
  if ((infile = fopen(filename, "r")) == NULL) {
    perror(filename);
    return -1;
  } /* error checking */

  while ((ch = fgetc(infile)) != EOF) { /* end of file */
    ungetc(ch, infile);
    
    count = 0;
    while ((ch = fgetc(infile)) != '\n') { /*stop at each line */
      if (ch == '\r') { /* combat with the CRLF nonsense */
        fgetc(infile);
        break;
      }
      ungetc(ch, infile);
      points[count] = scan_point(infile);
      count++;
    }
    play = new_triangle(points[0], points[1], points[2]);
    /*printf("loop\n");*/
  }
  printf("%d\n", play->incidented_edge->Twin->IncidentFace == NULL);

}


/* just a function to test */
void test(void){
  int iti, ni, san, yon;
  void *un, *deux, *trois;
  struct dcel_edge *one, *two, *three, *four, *five, *six;

  one = f_edge;
  two = f_edge->Next;
  three = two->Next;
  four = three->Next;
  five = four->Next;
  
  un = one->Twin->IncidentFace;
  deux = four->Twin->IncidentFace;
  printf("%g, %d\n",five->Origin->x, iti == ni);


}

struct dcel_vertex *scan_point(FILE *pos){
  double x, y;
  char ch;

  while (isspace(ch = fgetc(pos)));  // Skip whitespace
  ungetc(ch, pos);      // Put back the non-space character
  if (fscanf(pos, "(%lf,%lf)", &x, &y) == 2) /* be sure that it work */
  return new_vertex(x, y);
}   

struct dcel_face *new_triangle(struct dcel_vertex *p1, struct dcel_vertex *p2, struct dcel_vertex *p3){
  struct dcel_face *triangle_face;
  struct dcel_edge *edge1, *edge2, *edge3;
  triangle_face = malloc(sizeof(struct dcel_face));
  triangle_face->type = TRIANGLE;
  edge1 = new_edge(p1, p2);
  edge2 = new_edge(p2, p3);
  edge3 = new_edge(p3, p1);
  next_prev(edge1, edge2);
  next_prev(edge2, edge3);
  next_prev(edge3, edge1);
  edge1->IncidentFace = triangle_face;
  edge2->IncidentFace = triangle_face;
  edge3->IncidentFace = triangle_face;
  triangle_face->incidented_edge = edge1;
  return triangle_face;
}
