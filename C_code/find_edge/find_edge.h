#ifndef find_edge_H
#define find_edge_H

extern int **edge_graph;
extern int vertex_number;

void read_file(FILE *infile);
void add_edge(int ti1, int ti2, int ti3);
void print_result(int vertex_number);
void remove_border(int vertex_number);
void get_edges(int (*op)[3], int ntriangles);


#endif /* end of include guard: find_edge_H */

