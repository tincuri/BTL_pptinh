#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "dcel.h"
#include "misc.h"

/* some variable for stack */
struct node *head, *z;
/* face index of the 2 points */
/*int face1;*/
/*int face2;*/
/**/
int *dfsval;
bool done = false;
double angle(struct dcel_edge *edge1, struct dcel_edge *edge2){ /* return the angle between 2 edges */
  double x1, x2, x3, y1, y2, y3;
  double a1, a2, b1, b2;
  double angle;

  x1 = edge1->Origin->x;
  x2 = edge1->Twin->Origin->x;
  x3 = edge2->Twin->Origin->x;
  y1 = edge1->Origin->y;
  y2 = edge1->Twin->Origin->y;
  y3 = edge2->Twin->Origin->y;
  a1 = (x2 - x1);
  a2 = (y2 - y1);
  b1 = (x3 - x1);
  b2 = (y3 - y1);

  angle = atan2(b1, b2) - atan2(a1, a2);

  return angle;
}

/* insert a node (contains a half_edge) to the vertex linked list */
void insert_node(struct node *head, struct dcel_edge *half_edge){
  struct node *item;
  item = malloc(sizeof(struct node));
  item->half_edge = half_edge;
  item->next = head->next;
  head->next = item;
  return;
}

struct point *new_point(double x, double y){ /* the 2 points */
  struct point *p;
  p = malloc(sizeof(struct point));
  p->x = x; p->y = y;
  return p;
}

void connect(int x,int y, struct dcel_edge *h_edge){ /* function for connect node in a graph */
  struct graph_node *t;
  t = malloc(sizeof(struct graph_node ));
  t->node_index = x; t->edge = h_edge;
  t->next = face_graph[y]; face_graph[y] = t;
  t = malloc(sizeof(struct graph_node ));
  t->node_index = y; t->edge = h_edge;
  t->next = face_graph[x]; face_graph[x] = t;
  return;
}

enum orientation orientation(struct dcel_edge *h_edge, struct point *p){
  double x1, x2, x3, y1, y2, y3;
  double a1, a2, b1, b2;
  double cross_product;

  x1 = h_edge->Origin->x;
  x2 = h_edge->Twin->Origin->x;
  x3 = p->x;
  y1 = h_edge->Origin->y;
  y2 = h_edge->Twin->Origin->y;
  y3 = p->y;
  a1 = (x2 - x1);
  a2 = (y2 - y1);
  b1 = (x3 - x1);
  b2 = (y3 - y1);

  cross_product = a1 * b2 - a2 * b1;
  if (cross_product == 0)
    return LINE;
  if (cross_product > 0)
    return CCW;
  else return CW;
}

int point_location(struct point *p){
  int k = 0, strike = 0;
  struct dcel_edge *h_edge, *f_edge; 
  enum orientation o;

  for (;k < face_count; k++) {
    strike = 0;
    h_edge = face_list[k]->incidented_edge;
    f_edge = h_edge;
    do {
      o = orientation(h_edge, p);
      if (o == CCW) {
        strike++;
      } else break;
      h_edge = h_edge->Next;
    } while (h_edge != f_edge);
    if (strike == 3) {
      return k;
    }
  }
  printf("One of the points is probably outside the polygon\n");
  return k;
}

void find_sleeve(void){
  int k = face1;
  if (face1 >= face_count || face2 >= face_count) {
    printf("Failed\n");
    return ;
  }
  stack_init();
  listdfs();
  visit(k);
}

/* Depth-Fisrt Search */
void listdfs(void){
  int k;

  dfsval =malloc(vertex_count * sizeof(int));
  for (k = 0; k < vertex_count; k++) dfsval[k] = 0;
}

void visit(int k){
  struct graph_node *t;
  dfsval[k] = 1;
  if (done) {
    pop(); /* remove edge from the just checked node */
    return;
  }
  if (k == face2) {
    done = 1;
    return;
  }
  for (t = face_graph[k]; t != NULL; t = t->next)
    if (dfsval[t->node_index] == 0){
      push(t->edge);
      visit(t->node_index);
  }
  if (!done) {
    pop(); /* remove edge from the branch that failed */
  }
}

/////////////////////////////
/* some function for stack */
void push(struct dcel_edge *h_edge){
  struct node *item;
  item = malloc(sizeof(struct node));
  item->half_edge = h_edge;
  item->next = head->next;
  head->next = item;
}

void stack_init(void){
  head = malloc(sizeof(struct node));
  z = malloc(sizeof(struct node));
  head->next = z;
  z->next = z;
}

struct dcel_edge *pop(void){
  struct dcel_edge *key = head->next->half_edge;
  struct node *x = head->next;
  head->next = head->next->next;
  /*free(x);*/
  return key;
}

int stack_empty(void){
  return head->next == z;
}
////////////////////////

struct node *sort_edge(struct node *f_node){ 
  return MergeSort(f_node);
}

/* The code below is the linked list mergesort taken from geeksforgeeks */

// Function to split the singly linked list into two halves
struct node* split(struct node* head) {
    struct node* fast = head;
    struct node* slow = head;

    // Move fast pointer two steps and slow pointer
    // one step until fast reaches the end
    while (fast != NULL && fast->next != NULL) {
        fast = fast->next->next;
        if (fast != NULL) {
            slow = slow->next;
        }
    }

    // Split the list into two halves
    struct node* temp = slow->next;
    slow->next = NULL;
    return temp;
}

// Function to merge two sorted singly linked lists
struct node* merge(struct node* first, struct node* second) {
  
    // If either list is empty, return the other list
    if (first == NULL) return second;
    if (second == NULL) return first;

    // Pick the smaller value between first and second nodes
    if (first->angle < second->angle) {
        // Recursively merge the rest of the lists and
        // link the result to the current node
        first->next = merge(first->next, second);
        return first;
    }
    else {
        // Recursively merge the rest of the lists
        // and link the result to the current node
        second->next = merge(first, second->next);
        return second;
    }
}

// Function to perform merge sort on a singly linked list
struct node* MergeSort(struct node* head) {
  
    // Base case: if the list is empty or has only one node, 
    // it's already sorted
    if (head == NULL || head->next == NULL) {
        return head;
    }

    // Split the list into two halves
    struct node* second = split(head);

    // Recursively sort each half
    head = MergeSort(head);
    second = MergeSort(second);

    // Merge the two sorted halves
    return merge(head, second);
}
