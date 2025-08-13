from matplotlib import pyplot as plt
import pandas as pd

file_name = "2025_08_12_updated"

df = pd.read_csv(f"{file_name}.CSV")

plt.plot(df["Distances (m)"],df["Slope"])
plt.xlabel("Distance")
plt.ylabel("Slope")
plt.show()