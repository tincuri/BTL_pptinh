#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "dcel.h"
#include "misc.h"

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
  read_polygon_file(argv[1]);
  read_segment_file(argv[2]);
  return EXIT_SUCCESS;
}
