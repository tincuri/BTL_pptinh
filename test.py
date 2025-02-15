import matplotlib.pyplot as plt
import numpy as np

# Creating data points
x = np.linspace(0, 10, 100)
y = np.full_like(x, 0.8)

for _ in y:
    print(type(_))

# Plotting the line
plt.plot(x, y, label='y=0.8')
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('Plot of y=0.8')
plt.legend()
plt.grid(True)

# Display the plot
plt.show()
