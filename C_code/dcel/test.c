#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

void scan_point(FILE *pos);

int main(int argc, char *argv[])
{
  FILE *infile;
  char ch;
/* read the file */
  if ((infile = fopen(argv[1], "r")) == NULL) {
    perror(argv[1]);
    return -1;
  } /* error checking */

  /*do {*/
  /*  scan_point(infile);*/
  /*} while (fgetc(infile) != EOF);*/

  while ((ch = fgetc(infile)) != EOF) { /* end of file */
    ungetc(ch, infile);
    while ((ch = fgetc(infile)) != '\n') { /*stop at each line */
      if (ch == '\r') { /* combat with the CRLF nonsense */
        fgetc(infile);
        break;
      }
      /*printf("%d\n", ch);*/
      ungetc(ch, infile);
      scan_point(infile);
    }
    printf("line\n");
  }
    return EXIT_SUCCESS;
}


void scan_point(FILE *pos) {
  double x, y;
  char ch;
    
  while (isspace(ch = fgetc(pos)));  // Skip whitespace
  ungetc(ch, pos);      // Put back the non-space character
  
  if (fscanf(pos, "(%lf,%lf)", &x, &y) == 2) /* be sure that it work */
    printf("%g, %g | \n", x, y);
}


