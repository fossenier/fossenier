import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

# Existing data
iterations = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
    26, 27, 28, 29, 30, 31, 32, 33, 34, 35
]
times = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 2, 3, 5, 8, 12, 18, 28,
    44, 64, 97, 148, 221, 337, 513, 781, 1194, 1813
]

# New data
iterations += [
    36, 37, 38, 39, 40, 41, 42, 43, 44, 45
]
times += [
    2829, 4165, 6358, 9750, 14923, 22961, 35142, 53437, 81822, 127129
]

# Linear regression to extrapolate
X = np.array(iterations).reshape(-1, 1)
y = np.array(times)

# Create and train the model
model = LinearRegression()
model.fit(X, y)

# Extrapolating for iteration 75
predicted_time_75 = model.predict([[75]])[0]

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(iterations, times, marker='o', color='b', linestyle='-', linewidth=2, markersize=6)

# Plot the extrapolated value
plt.scatter(75, predicted_time_75, color='r', label=f'Extrapolated (75, {predicted_time_75:.2f} ms)')

# Adding labels and title
plt.title('Blink Iterations vs Time (ms)', fontsize=16)
plt.xlabel('Blink Iterations', fontsize=14)
plt.ylabel('Time (ms)', fontsize=14)

# Show grid and legend
plt.grid(True)
plt.legend()

# Display the plot
plt.show()

# Print the extrapolated value for iteration 75
print(f'Extrapolated Time for iteration 75: {predicted_time_75:.2f} ms')