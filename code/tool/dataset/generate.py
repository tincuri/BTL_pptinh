# -----------------------------------------------------------------------------
#   Randomly generate points in a [0,1) x [0,1) square and write to test.txt
# -----------------------------------------------------------------------------
import sys
import random
import math

# modified

# Prompt user to enter the number of vertices
# n = int(input("Number of vertices: "))
nn = [5, 10, 15, 20, 25, 50, 100, 150, 200, 400, 600, 1000]

# Minimum distance between points
min_dist = 1  # Adjust this to control sparsity

points = []

def is_far_enough(x, y):
    for px, py in points:
        if math.hypot(px - x, py - y) < min_dist:
            return False
    return True

for n in nn:
    while len(points) < n:
        x, y = random.randint(0, 100), random.randint(0, 100)
        if is_far_enough(x, y):
            points.append((x, y))

    # Write to file
    with open(f"./case_{n}.txt", "w") as f:
        f.write(f"{n}\n")
        for x, y in points:
            f.write(f"{x} {y}\n")




"""origin
import sys
import random

# prompt user to enter the number of vertices
n = int(input("Number of vertices: "))

f = open("test.txt", "w")
f.write("%i\n" % n)
for i in range(n):
    x = random.random()
    y = random.random()
    f.write("%f %f\n" % (x, y))
f.close()

"""