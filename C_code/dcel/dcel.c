#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include "dcel.h"

/*          uncomment to check              */
/*int main(int argc, char *argv[])*/
/*{*/
/*  struct dcel_vertex *o, *a, *c;*/
/*  double x;*/
/*  struct dcel_edge *D, *F, *G;*/
/*  struct node *t;*/
/**/
/*  o = new_vertex(0,1);*/
/*  a = new_vertex(2,3);*/
/*  c = new_vertex(4, 5);*/
/*  D = new_edge(o, a);*/
/*  F = new_edge(o, c);*/
/*  t = o->head->next;*/

/* loop through list */

/*  for (int i = 0; i < 3;t = t->next) { /* i is the time the loop hit head */
/*    if (t == o->head) i++;*/
/*    if (!(t == o->z || t == o->head)) { /* skip through the end and the head */
/*    D = t->half_edge;*/
/*    printf("node %g\n", D->Twin->Origin->x);*/
/*    }*/
/*  }*/
/*  /*x = o->head->next->half_edge->Twin->Origin->x;*/
/*  /*printf("%g\n", x);*/
/*  return EXIT_SUCCESS;*/
/*}*/

/* create a new vertex and return it */
struct dcel_vertex *new_vertex(double x, double y){
  struct dcel_vertex *new;
  new = malloc(sizeof(struct dcel_vertex));
  new->x = x;
  new->y = y;
  struct node *head, *z;
  new->head = malloc(sizeof(struct node));
  new->z = malloc(sizeof(struct node));
  new->z->next = new->head;/* make the list loop, (might change) */
  new->head->next = new->z;
  new->z->half_edge = NULL;
  return new;
}


/* create a new half_edge and its twin */
/* des for destination, org for origin, h_edge for half edge */
struct dcel_edge *new_edge(struct dcel_vertex *org, struct dcel_vertex *des){
  struct dcel_edge *h_edge, *twin;

  /* TODO: check if the edge has already been done */
  


  h_edge = malloc(sizeof(struct dcel_edge));
  twin = malloc(sizeof(struct dcel_edge));

  h_edge->Origin = org;
  h_edge->Twin = twin;
  h_edge->IncidentFace = NULL;
  twin->IncidentFace = NULL;
  insert_node(org->head, h_edge);

  twin->Origin = des;
  twin->Twin = h_edge;
  insert_node(des->head, twin);
  return h_edge;
}

/*struct dcel_face *new_triangle(struct dcel_vertex *p1, struct dcel_vertex *p2, struct dcel_vertex *p3){*/
/*  struct dcel_face *triangle_face;*/
/*  struct dcel_edge *edge1, *edge2, *edge3;*/
/*  triangle_face = malloc(sizeof(struct dcel_face));*/
/*  triangle_face->type = TRIANGLE;*/
/*  edge1 = new_edge(p1, p2);*/
/*  edge2 = new_edge(p2, p3);*/
/*  edge3 = new_edge(p3, p1);*/
/*  next_prev(edge1, edge2);*/
/*  next_prev(edge2, edge3);*/
/*  next_prev(edge3, edge1);*/
/*  edge1->IncidentFace = triangle_face;*/
/*  edge2->IncidentFace = triangle_face;*/
/*  edge3->IncidentFace = triangle_face;*/
/*  triangle_face->incidented_edge = edge1;*/
/*  return triangle_face;*/
/*}*/



/* insert a half_edge to the list */
void insert_node(struct node *head, struct dcel_edge *half_edge){
  struct node *item;
  item = malloc(sizeof(struct node));
  item->half_edge = half_edge;
  item->next = head->next;
  head->next = item;

}

void next_prev(struct dcel_edge *first, struct dcel_edge *next){
  first->Next = next;
  next->Prev = first;
}

/**/
/*struct dcel_vertex *next_vertex(struct dcel_vertex *vertex){*/
/*  return vertex->head->next->half_edge->Twin->Origin;*/
/*}*/
