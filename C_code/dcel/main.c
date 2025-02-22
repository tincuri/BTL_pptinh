#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "dcel.h"
#include "make_dcel.h"
#include "misc.h"
#include "scan.h"

int face1, face2; /* face index of the 2 points */

int main(int argc, char *argv[])
{
  if (argv[1] == NULL) {
    printf("Please input the polygon file\n");
    return -1;
  }
  if (argv[2] == NULL){
    printf("Please input the triagulated edges file\n");
    return -1;
  }
  if (argv[3] == NULL){
    printf("Please input the 2 points locations\n");
    return -1;
  }
  read_polygon_file(argv[1]);
  read_segment_file(argv[2]);
  read_point_file(argv[3]);
  create_dcel();
  find_sleve();
  return EXIT_SUCCESS;
}
void print_index(struct dcel_edge *h_edge){
  printf("(%g, %g)\n", h_edge->Origin->index, h_edge->Twin->Origin->index);
}
 
