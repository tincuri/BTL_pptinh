#ifndef h_dcel
#define h_dcel
/* TODO: create linked list for vertex to store list of incidentedge for faster queering --DONE--*/
/* TODO: change the liked list structure for mergesort */

/*          Structure           */

enum face {POLYGON, TRIANGLE, NONE};

struct dcel_vertex {
  double x;
  double y;
  struct node *head;/* head of the linked list */
  struct node *z; /* end of the linked list */
  int top; /* postion to put in the edge array */
  struct dcel_edge **edge_array; /* pointer to an array of edge */
};

struct dcel_edge {
  struct dcel_vertex *Origin;
  struct dcel_edge *Twin;
  struct dcel_face *IncidentFace;
  struct dcel_edge *Next;
  struct dcel_edge *Prev;
};

struct dcel_face {
  struct dcel_edge *incidented_edge; /* an edge that has it as IncidentFace */
  enum face type; /* if its a polygon face of a triangle face */
};

struct point { /* structure of the 2 points */
  struct dcel_face *InsideFace; /* the face where it lies */
};

struct node { /* structure of a linked list node */
  struct dcel_edge *half_edge;
  double angle; /* temporary angle use for the sorting step */
  struct node *next;
};



/*               Function prototype             */

struct dcel_vertex *new_vertex(double x, double y);
struct dcel_edge *new_edge(struct dcel_vertex *org, struct dcel_vertex *des);
/*struct dcel_face *new_triangle(struct dcel_vertex *p1, struct dcel_vertex *p2, struct dcel_vertex *p3);*/
/*struct dcel_vertex *next_vertex(struct dcel_vertex *vertex);, you should not find other vertex through a vertex, they only connected by edge*/
void next_prev(struct dcel_edge *first, struct dcel_edge *next);

/* linked list */
void insert_node(struct node *head, struct dcel_edge *half_edge);



/*            Global variable              */
extern int vertex_count; /* number of vertex of the polygon */
extern struct dcel_vertex **vertex_list; /* pointer to a list of vertex */


#endif /* ifndef h_dcel */
