# Implementing Lee & Preparata's shortest Euclidean path algorithm
This is a repository for our group's project for course "Numerical Methods" on presenting Lee and Preparata’s algorithm for finding shortest paths in a simple polygon.
The paper that we are implementing is ["Euclidean shortest paths in the presence of rectilinear barriers" by Lee and Preparata](https://www.semanticscholar.org/paper/Euclidean-shortest-paths-in-the-presence-of-Lee-Preparata/086cf6cb05ee77f0df9cccf8d3ec1328f0e9241f)
## Requirement
You will need:
- GCC (or a compiler of your choice, make sure to change the Makefile)
- make
- python
- numpy
- matplotlib

# Usage
## Triangulation
We offer 2 algorithms
### Seidel's algorithm
At `C_code/seidel-1.0` run `make` to build the binary file, run it without command line argument for the usage.
### Ear clipping
currently implementing
## Find the Sleeve
Because the difference between OSes, please rebuild the binary files. First, build the triangulation lib at `C_code/seidel-1.0`
```
make clean
make lib
```
Then, at `C_code/dcel`, you can choose one of the 2 binaries to build, one with build-in triangulation, and one without. The build-in triangulation algorithm is the Seidel's algorithm.

Choose one of the two lines below, the name should be clear enough.
```
make sleeve
make sleeve_no_tri
```
or without make, in `C_code/dcel` you can just compile all the file together with one of these command below:
```
gcc -lm main.c make_dcel.c dcel.c scan.c misc.c ../seidel-1.0/tri.c ../seidel-1.0/monotone.c ../seidel-1.0/construct.c ../seidel-1.0/misc.c ../find_edge/find_edge.c  -o sleeve
gcc -lm main_no_tri.c make_dcel.c dcel.c scan.c misc.c -o sleeve_no_tri
``` 
The code is not that long so it would not take to long to compile.

Now you can run the binary with the same name without command line arguments to get the usage. In `C_code` there is some sample files for how to structure your files.
## Lee & Preparata algorithm
In `code/lee.py` modify the files paths to your files paths, then run:
```
python code/lee.py
```
### Etc
There are some python functions for generating a polygon if you don't have one. Check out `code\README.md` for their usages.
## Acknowledgements
The [Seidel's algorithms](seidels-algorithm) is taken from [https://gamma.cs.unc.edu/SEIDEL/](https://gamma.cs.unc.edu/SEIDEL/) which was made by Atul Narkhede and Dinesh Manocha.
