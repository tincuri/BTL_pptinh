#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#include "find_edge.h"
#include "../seidel-1.0/triangulate.h"
int **edge_graph;
int vertex_number;
#ifdef STANDALONE

int main(int argc, char *argv[])
{
  FILE *infile;
  int triangles_number;
  int vertex_number;
  char *filename;
  char ch;

  if (argv[1] == NULL) {
    printf("Please input the triangles file\n");
    return -1;
  }
  filename = argv[1];
  if ((infile = fopen(filename, "r")) == NULL) {
    perror(filename);
    return -1;
  } /* error checking */
  fscanf(infile, "%d", &triangles_number);
  printf("%d\n", triangles_number);

  vertex_number = triangles_number + 2;
  edge_graph = malloc(vertex_number * sizeof(int *));
  for (int i = 0; i < vertex_number; i++) {
      edge_graph[i] = malloc(vertex_number * sizeof(int));
  }
  for (int i = 0; i < vertex_number; i++)
      for (int j = 0; j < vertex_number; j++)
          edge_graph[i][j] = 0; 
  read_file(infile);
  remove_border(vertex_number);
  print_result(vertex_number);
  return EXIT_SUCCESS;
}

#else

void get_edges(int (*op)[3], int ntriangles){
  int vertex_number;
  vertex_number = ntriangles + 2;
  edge_graph = malloc(vertex_number * sizeof(int *));
  for (int i = 0; i < vertex_number; i++) {
      edge_graph[i] = malloc(vertex_number * sizeof(int));
  }
  for (int i = 0; i < vertex_number; i++)
      for (int j = 0; j < vertex_number; j++)
          edge_graph[i][j] = 0; 
  for (int i = 0; i < ntriangles; i++) {
    add_edge(op[i][0], op[i][1], op[i][2]);
  }
  remove_border(vertex_number);

}

#endif /* ifdef STANDALONE */


void read_file(FILE *infile){
  int ti1, ti2, ti3;
  do {
    if (fscanf(infile, "%d %d %d", &ti1, &ti2, &ti3) == 3) {
      add_edge(ti1, ti2, ti3);
   }
  } while (fgetc(infile) != EOF);
}

void add_edge(int ti1, int ti2, int ti3){
    edge_graph[ti1][ti2] = 1;
    edge_graph[ti2][ti1] = 1;
    edge_graph[ti3][ti2] = 1;
    edge_graph[ti2][ti3] = 1;
    edge_graph[ti1][ti3] = 1;
    edge_graph[ti3][ti1] = 1;
}

void print_result(int vertex_number){
  int i, j;
  for (i = 0; i < vertex_number; i++) {
    for (j = 0; j <= i; j++) {
      if (edge_graph[i][j])
        printf("edge: %d %d\n", i, j);
    }
  }
}

void remove_border(int vertex_number){
  for (int i = 0; i < vertex_number - 1; i++) {
    edge_graph[i][i+1] = 0;
    edge_graph[i+1][i] = 0;
  }
  edge_graph[0][vertex_number - 1] = 0;
  edge_graph[vertex_number - 1][0] = 0;
}
