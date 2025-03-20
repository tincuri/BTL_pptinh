## Implementing Lee & Preparata's shortest Euclidean path algorithm
This is a repository for our group's project for course "Numerical Methods" on presenting Lee and Preparata’s algorithm for finding shortest paths in a simple polygon.
The paper that we are implementing is ["Euclidean shortest paths in the presence of rectilinear barriers" by Lee and Preparata](https://www.semanticscholar.org/paper/Euclidean-shortest-paths-in-the-presence-of-Lee-Preparata/086cf6cb05ee77f0df9cccf8d3ec1328f0e9241f)
### Requirement
You will need gcc (or a compiler of your choice, make sure to change the Makefile), make.

## Usage
Because the difference between OSes, please rebuild the binary files. 
First go to C_code/find_edge and build .o file
```
gcc -c find_edge.c
```
at C_code/seidel-1.0
```
make clean
make lib
```
at C_code/dcel, you can choose one of the 2 binaries to build, one with build-in triangulation, and one without. Choose one of the two lines below, the name should be clear enough
```
make sleeve
make sleeve_no_tri
```
Now you can run the binary with the same name (just run it dry for each usages) to get the sleeve by giving them some files.
