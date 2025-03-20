#ifndef scan_h
#define scan_h

/*         functions prototype         */
struct point *scan_point(FILE *pos);
struct dcel_vertex *scan_vertex(FILE *pos);
struct dcel_edge *scan_edge(FILE *pos);
struct point *new_point(double x, double y);
#endif /* ifndef scan_h */
