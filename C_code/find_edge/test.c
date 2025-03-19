
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    FILE *infile;
    int ch;  // Use int to store fgetc() result

    // Check if the user provided a file name
    if (argc < 2) {
        printf("Please input the file\n");
        return EXIT_FAILURE;
    }

    // Open the file for reading
    infile = fopen(argv[1], "r");
    if (infile == NULL) {
        perror("Error opening file");
        return EXIT_FAILURE;
    }

    // Read and print file contents
  fscanf(infile, "%d", ch);
  printf("%d\n", ch);

    // Close the file
    fclose(infile);

    return EXIT_SUCCESS;
}

