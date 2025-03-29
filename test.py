import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Data
x_data = np.array([2.07, 4.04, 6.00, 8.07, 10.04, 12.00, 14.08, 16.05, 18.07]) * -1
y_data = np.array([0.16, 0.35, 0.52, 0.69, 0.86, 1.03, 1.12, 1.37, 1.55]) * -1

# Model function
def model(x, a, b):
    return a * (np.exp(b * x) - 1)

# Initial guess
p0 = [0.01, 20]  # a = 0.01, b = 20

# Fit the model
params, covariance = curve_fit(model, x_data, y_data, p0=p0)
a, b = params
print(f"Fitted parameters: a = {a:.6f}, b = {b:.6f}")

# Generate smooth curve for plotting
x_smooth = np.linspace(min(x_data), max(x_data), 100)
y_smooth = model(x_smooth, a, b)

# Plot data and fitted curve
plt.scatter(x_data, y_data, color='blue', label='Data points')
plt.plot(x_smooth, y_smooth, color='red', label=f'Fit: y = {a:.3f}(e^{b:.3f}x - 1)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Nonlinear Least Squares Fit')
plt.legend()
plt.grid(True)
plt.show()