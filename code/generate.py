# -----------------------------------------------------------------------------
#   Randomly generate points in a [0,1) x [0,1) square and write to .txt
# -----------------------------------------------------------------------------

import random

# prompt user to enter the number of vertices
# n = int(input("Number of vertices: "))

nn = [200, 400, 600, 1000, 1200, 1400, 1600, 1800, 2000,2200, 2400]
for n in nn:
    f = open(f"dataset/vertices/case_{n}.txt", "w")
    f.write("%i\n" % n)
    for i in range(n):
        x = random.random()
        y = random.random()
        f.write("%f %f\n" % (x, y))
    f.close()
