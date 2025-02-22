#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include "dcel.h"
#include "misc.h"

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
  new->head->next = NULL;
  return new;
}


/* create a new half_edge and its twin */
/* des for destination, org for origin, h_edge for half edge */
struct dcel_edge *new_edge(struct dcel_vertex *org, struct dcel_vertex *des){
  struct dcel_edge *h_edge, *twin;

  h_edge = malloc(sizeof(struct dcel_edge));
  twin = malloc(sizeof(struct dcel_edge));

  h_edge->Origin = org;
  h_edge->Twin = twin;
  h_edge->IncidentFace = NULL;
  h_edge->connected = false;
  insert_node(org->head, h_edge);

  twin->Origin = des;
  twin->Twin = h_edge;
  twin->IncidentFace = NULL;
  twin->connected = false;
  insert_node(des->head, twin);

  return h_edge;
}

void next_prev(struct dcel_edge *first, struct dcel_edge *next){
  first->Next = next;
  next->Prev = first;
}
