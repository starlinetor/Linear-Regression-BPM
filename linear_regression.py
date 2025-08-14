from cProfile import label
from matplotlib import pyplot as plt
from numpy import var
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from tabulate import tabulate

file_name = "2025_08_12_updated"

df = pd.read_csv(f"{file_name}.CSV")

variables : list[str] = ["Slope", "Altitude (m)", "Distances (m)", "Time (s)",  "Speed (m/s)",]

x = df[variables]
y = df["HR (bpm)"]

x_train, x_test, y_train, y_test = train_test_split(x,y)
model = LinearRegression()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)

rounded_model_coef : list[float] = []
for coef in model.coef_:
    rounded_model_coef.append(float(round(coef,4)))

standard_coef_impact : list[float] = []
for coef, variable in zip(model.coef_ , variables):
    standard_coef_impact.append(float(round(coef * (max(df[variable])-min(df[variable])),4)))
    
print("Intercept:", model.intercept_)
print("Mean squared error: %.4f" % mean_squared_error(y_test, y_pred))
print("Coefficient of determination (R²): %.4f" % r2_score(y_test, y_pred))

row_1 : list = ["Model coef"] + rounded_model_coef
row_2 : list = ["S. coef impact"] + standard_coef_impact

print(tabulate([variables,row_1, row_2], headers="firstrow", tablefmt="github"))

y_full_pred = model.predict(x)

plt.plot(df["Distances (m)"],y_full_pred, color = "r", label = "predicted")
plt.plot(df["Distances (m)"],y, color = "b", label = "real")
plt.xlabel("Time")
plt.ylabel("HR")
plt.show()