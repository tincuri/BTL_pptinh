#ifndef h_dcel
#define h_dcel

/*          Structure           */

enum face {OUTSIDE, TRIANGLE, NONE};

struct dcel_vertex {
  double x;
  double y;
  int index; /* the index of the vertex in the vertex_list */
  struct node *head;/* head of the linked list */
};

struct dcel_edge {
  struct dcel_vertex *Origin;
  struct dcel_edge *Twin;
  struct dcel_face *IncidentFace;
  struct dcel_edge *Next;
  struct dcel_edge *Prev;
  bool connected; /* boolean to check if a graph connection has been added through the edge*/
};

struct dcel_face {
  struct dcel_edge *incidented_edge; /* an edge that has it as IncidentFace */
  enum face type; /* if its a polygon face of a triangle face */
  int index; /* index of the face in the graph list */
};

/*               Function prototype             */

struct dcel_vertex *new_vertex(double x, double y);
struct dcel_edge *new_edge(struct dcel_vertex *org, struct dcel_vertex *des);
void next_prev(struct dcel_edge *first, struct dcel_edge *next);


/*            Global variable              */

extern int vertex_count; /* number of vertex of the polygon */
extern int hole_count; /* number of holes */
extern int face_count; /* number of face */
extern struct dcel_vertex **vertex_list; /* pointer to a list of vertex */
extern struct dcel_face **face_list;
extern struct graph_node **face_graph; /* dual graph of the polygon */
extern struct dcel_vertex *first; /* first vertex */
extern struct dcel_edge *f_edge; /* first edge */
extern struct dcel_edge **pi_path; /* a stack of h_edge for pi_pat */
extern int *dfsval;
/* face index of the 2 points */
extern int face1;
extern int face2;
/* variable for stack */
extern struct node *head, *z; 

#endif /* ifndef h_dcel */
