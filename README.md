## Implementing Lee & Preparata's shortest Euclidean path algorithm
This is a repository for our group's project for course "Numerical Methods" on presenting Lee and Preparata’s algorithm for finding shortest paths in a simple polygon.
The paper that we are implementing is ["Euclidean shortest paths in the presence of rectilinear barriers" by Lee and Preparata](https://www.semanticscholar.org/paper/Euclidean-shortest-paths-in-the-presence-of-Lee-Preparata/086cf6cb05ee77f0df9cccf8d3ec1328f0e9241f)
### Requirement
You will need gcc (or a compiler of your choice, make sure to change the Makefile), make.

## Usage
### Find the Sleeve
Because the difference between OSes, please rebuild the binary files. First, build the triangulation lib at C_code/seidel-1.0
```
make clean
make lib
```
Then, at C_code/dcel, you can choose one of the 2 binaries to build, one with build-in triangulation, and one without. Choose one of the two lines below, the name should be clear enough
```
make sleeve
make sleeve_no_tri
```
or without make, in C_code\dcel you can just compile all the file together with one of these command below
```
gcc -lm main.c make_dcel.c dcel.c scan.c misc.c ../seidel-1.0/tri.c ../seidel-1.0/monotone.c ../seidel-1.0/construct.c ../seidel-1.0/misc.c ../find_edge/find_edge.c  -o sleeve
gcc -lm main_no_tri.c make_dcel.c dcel.c scan.c misc.c -o sleeve_no_tri
```
The code is not that long so it would not take to long to compile.
Now you can run the binary with the same name (just run it dry for the usage) to get the sleeve by giving them some files.
