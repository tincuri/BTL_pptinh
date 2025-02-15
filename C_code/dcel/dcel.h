#ifndef h_dcel
#define h_dcel
/* TODO: create linked list for vertex to store list of incidentedge for faster queering --DONE--*/


/*          Structure           */
struct dcel_vertex {
  double x;
  double y;
  struct node *head;/* head of the linked list */
  struct node *z; /* end of the linked list */
};

struct dcel_edge {
  struct dcel_vertex *Origin;
  struct dcel_edge *Twin;
  struct dcel_face *IncidentFace;
  struct dcel_edge *Next;
  struct dcel_edge *Prev;
};

struct dcel_face {
  bool Inside; /* if it is outside or inside the polygon */
};

struct point { /* structure of the 2 points */
  struct dcel_face *InsideFace; /* the face where it lies */
};

struct node { /* structure of a linked list node */
  struct dcel_edge *half_edge;
  struct node *next;
};



/*               Function prototype             */

struct dcel_vertex *new_vertex(double x, double y);
struct dcel_edge *new_edge(struct dcel_vertex *org, struct dcel_vertex *des);
struct dcel_edge *new_polygon_edge(struct dcel_vertex *org, struct dcel_vertex *des);
/*struct dcel_vertex *next_vertex(struct dcel_vertex *vertex);, you should not find other vertex through a vertex, they only connected by edge*/
void next_prev(struct dcel_edge *first, struct dcel_edge *next);

/* linked list */
void insert_node(struct node *head, struct dcel_edge *half_edge);



/*            Global variable              */
extern int vertex_count; /* number of vertex of the polygon */


#endif /* ifndef h_dcel */
