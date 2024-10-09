
#* This script generates base station data in YAML format: (Slice data generated in slice_data.yaml)
#* Replace the base-station and slice yaml data with example data for slicesim (+adjust other parameters for graphing)

import random

# Constants
num_slices = 1000
base_station_count = 30
x_range = (0, 1980) 
y_range = (0, 1980)

# Generate the base station YAML configuration
base_stations_yaml = "base_stations:\n"

for i in range(base_station_count):
    base_station_entry = f"  - capacity_bandwidth: 20000000000\n"  
    base_station_entry += f"    coverage: {200 + i * 10}\n"  
    base_station_entry += f"    ratios:\n"
    
    # Add slice ratios
    for j in range(1, num_slices + 1):
        base_station_entry += f"      slice_{j}: 0.001\n"
    
    # Generate random x and y coordinates
    x_coordinate = random.randint(*x_range)
    y_coordinate = random.randint(*y_range)
    
    base_station_entry += f"    x: {x_coordinate}\n"  # Random x coordinate
    base_station_entry += f"    y: {y_coordinate}\n"  # Random y coordinate
    
    base_stations_yaml += base_station_entry

# Save the generated YAML to a text file
with open("base_stations.yaml", "w") as file:
    file.write(base_stations_yaml)

print("Base stations YAML configuration has been saved to base_stations.yaml.")
