
lower_branch = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]



for index in range(-1, -len(lower_branch), -1):  # Iterate backwards
    print(lower_branch[index], lower_branch[index-1])

index = 4
del lower_branch[4:]
print(lower_branch)