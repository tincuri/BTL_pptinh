#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <ctype.h>

#include "dcel.h"
#include "misc.h"
#include "make_dcel.h"
#include "scan.h"

/* TODO: make the graph --kinda done--*/
/* rememeber to remove the z node later */

int vertex_count = 0; /* number of vertices */
int hole_count = 0; /* number of holes */
int face_count;
int rk = 0; /* global counter for recursion stuff*/
struct dcel_vertex **vertex_list; /* list of vertex */
struct dcel_face **face_list; /* list of faces */
struct graph_node **face_graph; /* graph of faces connection*/
struct dcel_vertex *first; /* first vertex */
struct dcel_edge *f_edge; /* first edge */
struct point test_point2 = {.x = 0.085, .y = 0.644};
struct point test_point1 = {.x = 0.9, .y = 0.27};
void print_edge(struct dcel_edge *h_edge);
void test(void);
void print_index(struct dcel_edge *h_edge);

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
  face1 = point_location(&test_point1);
  face2 = point_location(&test_point2);
  /*face1 = 0;*/
  /*face2 = 9;*/
  find_sleeve();
  printf("vertex count %d\n", vertex_count);
  printf("%d, %d\n", face1, face2);
  test();
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
  first = scan_vertex(infile);
  second = scan_vertex(infile);
  one = second;
  vertex_count += 2; /* for the 2 vertex needed for the 1st edge */

  edge1 = new_edge(first, second);
  f_edge = edge1;

  while ((ch = fgetc(infile)) != '\n') { /*stop at each line */
      if (ch == '\r') { /* combat with the CRLF nonsense */
        fgetc(infile);
        break;
      }
      ungetc(ch, infile);

      two = scan_vertex(infile);
      edge2 = new_edge(one, two);  
      next_prev(edge1, edge2);
      edge1 = edge2;
      one = two;
      vertex_count++;
    }

  l_edge = new_edge(one, first); /* last edge */
  next_prev(edge2, l_edge);
  next_prev(l_edge, f_edge);


  vertex_list = malloc(vertex_count*sizeof(struct dcel_vertex*)); /* make the vertex list */
  int i = 0;
  
  edge1 = f_edge;
  do { /* make it loop once */
    vertex_list[i] = edge1->Origin;
    vertex_list[i]->index = i;
    edge1 = edge1->Next;
    i++;
  } while (edge1 != f_edge);

  return vertex_count;

}

/* read the edge file and add those edge */
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


  while ((ch = fgetc(infile)) != '\n') { /*stop at each line */
    if (ch == '\r') { /* combat with the CRLF nonsense */
      fgetc(infile);
      break;
    }
    ungetc(ch, infile);
    test = scan_edge(infile);
    count++;
  }
  /*printf("%d\n", count);*/

}

void create_dcel(void){
  struct dcel_vertex **copy = vertex_list; /* prepare if I messed up and break the vertex_list */
  struct dcel_vertex *check;/* the vertex that getting checked */
  struct dcel_edge *edge;
  struct node *t, *p, *head;/* node for easy traversal */
  struct node *f_node, *l_node; /* first and last node */

  
  for (int i = 0; i < vertex_count;i++) {
    check = copy[i];
    head = check->head;
    f_node =head->next;
    t = head;
    int j; /* counter */
    for (j = 0;t != NULL; t = t->next, j++); /* count the numbers of edge that have Origin as that point */
    /* compute the angle for each edge */
    f_node->angle = 0; /* let the first edge as the initial side */
    for (t = f_node->next; t != NULL; l_node = t, t = t->next) {
      t->angle = angle(f_node->half_edge, t->half_edge);
    }
    l_node->angle = angle(f_node->half_edge, l_node->half_edge);
   
    f_node = sort_edge(f_node);
    copy[i]->head->next  = f_node;

    /* make prev and twin */
    for (p = f_node, t = f_node->next; t != NULL;p = t, t = t->next) {
      p->half_edge->Twin->Next = t->half_edge;
      t->half_edge->Prev = p->half_edge->Twin;
    }
    p->half_edge->Twin->Next = f_node->half_edge;
    f_node->half_edge->Prev = p->half_edge->Twin;
  }

  /* face & graph */
  make_dual_graph();
}

/* make the faces and its dual graph */
void make_dual_graph(void){
  struct node *t, *head;
  struct dcel_edge *h_edge;
  struct dcel_face *face;
  struct graph_node *z;
  face_count = vertex_count - 2 - 2 * hole_count;
  face_graph = malloc(face_count * sizeof(struct graph_node *));
  face_list = malloc((face_count + 1) * sizeof(struct dcel_face *));

  /* init graph */

  z = malloc(sizeof(struct graph_node*));
  for (int j; j < face_count; j++) face_graph[j] = NULL;

  /* mark the outside face */
  h_edge = f_edge->Twin;
  face = malloc(sizeof(struct dcel_face));
  face->type = OUTSIDE;
  do {
    h_edge->IncidentFace = face;
    h_edge = h_edge->Next;
  } while (h_edge != f_edge->Twin);
  face->incidented_edge = h_edge;
  face_list[face_count] = face;

  /* mark the other face and make the graph */
  h_edge = f_edge;
  recursion_face(h_edge);
  /*printf("%d\n", rk);*/
}

void recursion_face(struct dcel_edge *h_edge){
  struct dcel_face *face;
  struct dcel_edge *f_edge = h_edge;
  
  if (h_edge->IncidentFace != NULL) {
    return;
  }
  face = malloc(sizeof(struct dcel_face));
  face->type = TRIANGLE;
  h_edge->IncidentFace = face; 
  face->incidented_edge = h_edge;
  face_list[rk] = face;

  face->index = rk++;
  connect_face(h_edge);
  do {
    h_edge->IncidentFace = face; 
    h_edge = h_edge->Next;
  } while (h_edge != f_edge);
  recursion_face(h_edge->Next->Twin);
  recursion_face(h_edge->Next->Next->Twin);
  return;
}

void connect_face(struct dcel_edge *h_edge){
  struct dcel_edge *twin = h_edge->Twin;
  if (twin->IncidentFace == NULL || twin->IncidentFace->type == OUTSIDE || h_edge->connected == true ) {
    return;
  } /* condition */

  connect(h_edge->IncidentFace->index, twin->IncidentFace->index, h_edge);
  return;
}


/* just some functions to test and debug*/
void test(void){
  int iti, ni, san, yon, index;
  struct dcel_vertex *un, *deux, *trois;
  struct dcel_edge *one, *two, *three, *four, *five, *six;
  struct dcel_face *f_face, *test_face;
  struct node *t;
  struct graph_node *f_node;
  one = f_edge;
  two = f_edge->Next;
  f_face = one->IncidentFace;
  index = f_face->index;
  f_node = face_graph[index];
  f_node = face_graph[f_node->node_index];
  f_node = face_graph[4];
  /**/
  /*for (; f_node != NULL; f_node = f_node->next) {*/
  /*  printf("%d ", f_node->node_index);*/
  /*  print_edge(f_node->edge);*/
  /*}*/
  /*iti = 0;*/
  /*for (; iti < face_count; iti++) {*/
  /*  f_node = face_graph[iti];*/
  /*  printf("%d ", iti);*/
  /*  for (; f_node != NULL; f_node = f_node->next) {*/
  /*    printf("%d", f_node->node_index);*/
  /*    /*print_edge(f_node->edge);*/
  /*  }*/
  /*  printf("| ");*/
  /*}*/
  /*test_face = point_location(&test_point);*/
  /*printf("%d\n", test_face->index);*/
 
  for ( t = head->next; t != z; t = t->next) {
    print_edge(t->half_edge);
  }
}
void print_index(struct dcel_edge *h_edge){
  printf("(%d, %d)\n", h_edge->Origin->index, h_edge->Twin->Origin->index);
}
void print_edge(struct dcel_edge *h_edge){
  printf("(%g, %g) - (%g, %g)\n", h_edge->Origin->x, h_edge->Origin->y, h_edge->Twin->Origin->x, h_edge->Twin->Origin->y);
}
