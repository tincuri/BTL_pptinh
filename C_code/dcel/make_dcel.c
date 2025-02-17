#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <ctype.h>

#include "dcel.h"
#include "misc.h"
#include "make_dcel.h"
#include "scan.h"

/*        TODO: make a scan_point function to read the file             */

int vertex_count = 0;
struct dcel_vertex **vertex_list;
struct dcel_vertex *first; /* first vertex */
struct dcel_edge *f_edge; /* first edge */

void test(void);


int main(int argc, char *argv[])
{
  if (argv[1] == NULL) {
    printf("Please input the polygon file\n");
    return -1;
  }
  if (argv[2] == NULL) {
    printf("Please input the edge file\n");
    return -1;
  }
  read_polygon_file(argv[1]);
  read_edge_file(argv[2]);
  create_dcel();
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


  vertex_list = malloc(vertex_count*sizeof(struct dcel_vertex*)); /* make the vertex list */
  int i = 0;
  
  edge1 = f_edge;
  do { /* make it loop once */
    vertex_list[i] = edge1->Origin;
    edge1 = edge1->Next;
    i++;
  } while (edge1 != f_edge);

  return vertex_count;

}

/* read the edge file and add them */
int read_edge_file(char *filename){

  FILE *infile;
  struct dcel_vertex *points[3], *try; /* list of 3 points */
  char ch;
  int count = 0;
  struct dcel_edge *test;

  /* read the file */
  if ((infile = fopen(filename, "r")) == NULL) {
    perror(filename);
    return -1;
  } /* error checking */

  printf("\n");

  while ((ch = fgetc(infile)) != '\n') { /*stop at each line */
    if (ch == '\r') { /* combat with the CRLF nonsense */
      fgetc(infile);
      break;
    }
    ungetc(ch, infile);
    test = scan_edge(infile);
    count++;
    printf("%g\n", test->Origin->x);
  }
  printf("%d\n", count);

}

void create_dcel(void){
  struct dcel_vertex **copy = vertex_list;
  struct dcel_vertex *check;/* the vertex that getting checked */
  struct dcel_edge *edge;
  struct node *t;
  struct dcel_edge **edge_list;
  
  int i, j, k; /* counters */
  i = 0;
  for (; i < vertex_count;i++) {
    check = copy[i];
    t = check->head;
    for (j = 0;t != check->z; t = t->next, j++); /* count the numbers of edge that have Origin as that point */
    edge_list = malloc(j * sizeof(struct dcel_edge*));
    t = check->head->next;
    /* make the edge list */
    for (k = 0; k < j; t = t->next, k++) {
      edge_list[k] = t->half_edge;
    }
    /* compute the angle for each edge */
    edge_list[0]->angle = 0; /* take the first edge as the initial side */
    for (k = 1; k < j; k++) {
      edge_list[k]->angle = angle(edge_list[0], edge_list[k]); /* measure the angle of the edges to the first one */
    }

    sort_edge(edge_list);
    check->edge_array = edge_list;
  }
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
  
  for (int i = 0; i < vertex_count; i++) {
    printf("%g\n", vertex_list[i]->x );
  }
}
   

