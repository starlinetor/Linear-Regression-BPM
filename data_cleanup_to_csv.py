from math import floor
import pandas as pd
import numpy as np
import time
import datetime

file_name = "2025_08_12"

df = pd.read_csv(f"{file_name}.CSV", usecols=[1,2,3,6,8])

altitude_data = df["Altitude (m)"]
distance_data = df["Distances (m)"]
time_data = df["Time"]

#time step for the slope calculation
data_size = len(altitude_data)
slope_data = np.zeros(data_size, dtype=float)
delta_distance : int = 100

#create slope data
print("\nCalculating slope data")
for i in range(data_size):
    if i%int(data_size/20)==0:
        print(f"{i/data_size*100:.2f}%")
    j : int = i
    while True:
        if j < 0:
            j= j+10
            break
        distance = distance_data[i] - distance_data[j]
        if distance >= delta_distance:
            break
        j = j-10
            
    n = (altitude_data[i] - altitude_data[j])
    d = distance 
    slope_data[i] = n/d if d != 0 else 0

print("Finished calculating slope data\n")

df.insert(len(df.columns), "Slope", slope_data)

#speed data info
max_delta_time : int = 500
speed_data = np.zeros(data_size, dtype=float)

print("Calculating speed data")

#time is calculated in seconds, each time step is in seconds
for i in range(data_size):
    if i%int(data_size/20)==0:
        print(f"{i/data_size*100:.2f}%")
    delta_time = max_delta_time if i >= max_delta_time else i
    
    n = distance_data[i] - distance_data[i-delta_time]
    d = delta_time

    speed_data[i] = n/d if d != 0 else 0

print("Finished calculating speed data\n")

df.insert(len(df.columns), "Speed (m/s)", speed_data)

df["Speed converted (km/h)"] = df["Speed (km/h)"]/3.6


time_data_seconds = np.zeros(data_size, dtype=int)
#edit time format
start_time : int = 95
for i in range(data_size):
    x = time.strptime(time_data[i], "%H:%M:%S")
    time_data_seconds[i] = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds() - start_time

#check for missing data
print("Missing data in the csv")
for column in df.columns:
    missing_data = df[column].isna()
    print(f"{column} : {missing_data.sum()}")
    if missing_data.sum() == 0:
        continue
    missing_data_list = df[missing_data].index.tolist()
    for i in missing_data_list:
        j : int = 0
        out_of_bounds : bool = False
        while True:
            index = int(-j/2) if j%2==0 else floor(j/2)
            if not (0 <= i+j < data_size):
                if not out_of_bounds :
                    out_of_bounds = True
                else :
                    raise RuntimeError(f"Couldn't fix data in {column}\nUnfixable data has index {i}")
                j = j+1
                continue
            out_of_bounds = False
            if i+j in missing_data_list:
                j = j+1
            else:
                df.loc[i, column] = df[column][i+j]
                break
print("Fixed missing data \n")

df.insert(1,"Time (s)",time_data_seconds)
print(df)

df.to_csv(f"{file_name}_updated.CSV")



