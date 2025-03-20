#ifndef make_dcel_h
#define make_dcel_h

/*          Function prototype          */

int read_polygon_file(char *filename);
int read_edge_file(char *filename);
void create_dcel(void);
void make_dual_graph(void);
void recursion_face(struct dcel_edge *h_edge);
void connect_face(struct dcel_edge *h_edge);

#endif /* ifndef make_dcel_h */
