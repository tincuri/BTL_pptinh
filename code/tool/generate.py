# -----------------------------------------------------------------------------
#   Randomly generate points in a [0,1) x [0,1) square and write to test.txt
# -----------------------------------------------------------------------------
import sys
import random
import math

# file an cap, dang nghi recursive method

"""# recursion method: for the future

# Prompt user to enter the number of vertices
n = int(input("Number of vertices: "))

# Minimum distance between points
min_dist = 0.1  # Adjust this to control sparsity

points = []

def is_far_enough(x, y):
    for px, py in points:
        if math.hypot(px - x, py - y) < min_dist:
            return False
    return True

# separate n:"""



# Prompt user to enter the number of vertices
n = int(input("Number of vertices: "))

# Minimum distance between points
min_dist = 0.1  # Adjust this to control sparsity

points = []

def is_far_enough(x, y):
    for px, py in points:
        if math.hypot(px - x, py - y) < min_dist:
            return False
    return True

while len(points) < n:
    x, y = random.random(), random.random()
    if is_far_enough(x, y):
        points.append((x, y))

# Write to file
with open("test.txt", "w") as f:
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