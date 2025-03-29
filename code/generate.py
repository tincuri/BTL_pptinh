# -----------------------------------------------------------------------------
#   Randomly generate points in a [0,1) x [0,1) square and write to .txt
# -----------------------------------------------------------------------------

import random

# prompt user to enter the number of vertices
# n = int(input("Number of vertices: "))
nn = [5, 10, 15, 20, 25, 50, 100, 150, 200, 400, 600, 1000, 2000, 4000, 10000]

for n in nn:
    f = open(f"code/dataset/vertices/case_{n}.txt", "w")
    f.write("%i\n" % n)
    for i in range(n):
        x = random.random()
        y = random.random()
        f.write("%f %f\n" % (x, y))
    f.close()
