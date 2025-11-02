import matplotlib.pyplot as plt

# details of the ship
mass = 400          # tons, could change for different ship
width = 36          # meters, could change for different ship
force = 225.873     # N, thruster output, assuming this is constant
speed = 0           # m/s, starts 0 then increases

# force opposing thrusters
def drag(speed):
    return width*speed*(speed + 60)/4800 + force*mass/(mass+10000) + 10

# in m/s^2
def acceleration(speed):
    return (force - drag(speed)) / mass

# simulation
dt = 1  # time step in seconds
time = 0
times = [time]
speeds = [speed]

while True:
    a = acceleration(speed)
    speed += a * dt
    time += dt

    times.append(time)
    speeds.append(speed)

    # stop when acceleration is nearly zero (terminal velocity reached)
    if abs(a) < 1e-2:
        break

# convert time to minutes if long
if max(times) > 600:
    times = [t/60 for t in times]
    time_label = "Time (minutes)"
else:
    time_label = "Time (seconds)"

# plot
plt.figure(figsize=(8,5))
plt.plot(times, speeds, label="Speed vs Time")
plt.xlabel(time_label)
plt.ylabel("Speed (m/s)")
plt.title("Ship Speed Over Time")
plt.grid(True)
plt.legend()
plt.show()