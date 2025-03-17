#ifndef misc_h
#define misc_h

/*       Structure        */

enum orientation { CCW, LINE, CW }; /* enum for the orientation of the points */

struct point { /* structure of the 2 points */
  double x;
  double y;
  struct dcel_face *InsideFace; /* the face where it lies */
};

struct node { /* structure of a linked list node */
  struct dcel_edge *half_edge;
  double angle; /* temporary angle use for the sorting step */
  struct node *next;
};

struct graph_node {
  int node_index;
  struct graph_node *next;
  struct dcel_edge *edge;
};

/*         functions prototype         */

double angle(struct dcel_edge *edge1, struct dcel_edge *edge2);
struct node *sort_edge(struct node *f_node);
enum orientation orientation(struct dcel_edge *h_edge, struct point *p);
int point_location(struct point *p);
/* Basic datastructure */

/* linked list */
void insert_node(struct node *head, struct dcel_edge *half_edge);
/* graph */
void connect(int i, int j, struct dcel_edge *h_edge);
struct point *new_point(double x, double y);
void find_sleeve(void);
/* stack */
void push(struct dcel_edge *h_edge);
struct dcel_edge *pop(void);
void stack_init(void);
int stack_empty(void);
/* DFS */
void listdfs(void);
void visit(int k);
/* mergesort */
struct node *split(struct node *head);
struct node *merge(struct node *first, struct node *second);
struct node *MergeSort(struct node *head);

#endif /* ifndef misc_H */
