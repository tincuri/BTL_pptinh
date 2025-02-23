#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include "dcel.h"
#include "misc.h"

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
