from matplotlib import pyplot as plt
import pandas as pd

file_name = "2025_08_12_updated"

df = pd.read_csv(f"{file_name}.CSV")

plt.plot(df["Time (s)"],df["Speed (m/s)"], color = "r", label = "Calculated")
#plt.plot(df["Time (s)"],df["Speed converted (km/h)"], color = "b", label = "Registered")
#plt.plot(df["Time (s)"],df["Speed (km/h)"], color = "g", label = "Registered km")
plt.xlabel("Time")
plt.ylabel("Speed")
plt.show()