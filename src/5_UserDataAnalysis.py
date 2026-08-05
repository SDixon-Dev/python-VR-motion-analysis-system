#imports the various modules and libraries required
import triad_openvr  # for VR device interaction
import time  # for time-related functions
import sys  # for system-specific parameters and functions
import pandas as pd  #pandas library for data manipulation
import csv  # csv module for reading and writing CSV files
from pathlib import Path

# Locate the root folder of the repository.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define the expert reference and generated user-data paths.
PRO_DATA_PATH = PROJECT_ROOT / "sample_data" / "ProData.csv"
USER_DATA_PATH = PROJECT_ROOT / "data" / "UserData.csv"

# Function to record positional data of VR controllers and save it to a CSV file
def record_pose_data(file_path, interval, move_length):
    v = triad_openvr.triad_openvr()  # Initialise
    v.print_discovered_objects()  # Printing discovered VR objects
    
    data = []  # List to store positional data
    
    # Define column names for the DataFrame
    columns = ['x1', 'y1', 'z1','yaw1','pitch1','roll1','x2','y2','z2','yaw2','pitch2','roll2']
    # Create an empty DataFrame with defined columns
    posDf = pd.DataFrame(columns=columns)  
    
    start_time = time.time()  # Record the start time of the recording process
    
    # Loop to continuously record data until move_length is reached
    while True:
        start = time.time()  # Record the start time of each loop
        
        txt = ""  # Empty string to store pose data
        pose_data = {}  # Dictionary to store pose data for each device
        controller_array = []  # List to store pose data for both controllers
        
        # Loop through each VR controller device
        for device_name in ["controller_1", "controller_2"]:
            pose = v.devices[device_name].get_pose_euler()  # Get pose data for the controller
            controller_array += pose  # Appends to the controller array
            pose_data[device_name] = pose  # Stores them in the dictionary
            
            # Append pose data to the text string for printing
            for each in pose:
                txt += "%.4f" % each
                txt += " "
        print("\r" + txt, end="")  # Print the pose data
        
        data.append(pose_data)  # Append pose data to the main data list
        
        # Create a new row for the DataFrame with controller pose data
        new_controller_row = {"x1": controller_array[0], "y1": controller_array[1], "z1": controller_array[2],
                              "yaw1": controller_array[3], "pitch1": controller_array[4], "roll1": controller_array[5],
                              "x2": controller_array[6], "y2": controller_array[7], "z2": controller_array[8],
                              "yaw2": controller_array[9], "pitch2": controller_array[10], "roll2": controller_array[11]}
        posDf.loc[len(posDf)] = new_controller_row  # Append the new row to the DataFrame
        
        # Calculate the remaining sleep time to maintain the desired interval
        sleep_time = interval - (time.time() - start)
        
        # Check if move_length is reached, if so, break the loop
        if time.time() - start_time >= move_length:
            print("Move finished!")
            break
        
        # If there's remaining sleep time, wait before the next loop iteration
        if sleep_time > 0:
            time.sleep(sleep_time)
    
    # Convert the supplied location into a Path object.
    file_path = Path(file_path)

    # Create the destination folder if it does not already exist.
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the user's recorded motion data.
    posDf.to_csv(file_path, index=False)

# Function to calculate the average distance between corresponding values in two CSV files
def calculate_file_score(test_file, target_file):
    column_distances = []  # List to store the differences between corresponding values
    column_names = []  # List to store column names
    
    # Open both test and target CSV files for reading
    with open(test_file, 'r') as test_f, open(target_file, 'r') as target_f:
        test_reader = csv.reader(test_f)  # Create a CSV reader for the test file
        target_reader = csv.reader(target_f)  # Create a CSV reader for the target file
        
        test_header = next(test_reader)  # Store the header row of the test file
        target_header = next(target_reader)  # Skip the header row of the target file
        
        # Loop through each pair of corresponding column names and append them to the list
        for test_val, target_val in zip(test_header, target_header):
            column_names.append(test_val)
        
        # Loop through each row in both files
        for test_row, target_row in zip(test_reader, target_reader):
            # Loop through each pair of corresponding values in the rows
            for test_val, target_val in zip(test_row, target_row):
                # Convert values to floats and calculate the difference
                test_val = float(test_val)
                target_val = float(target_val)
                distance = test_val - target_val  # Retain sign of the difference
                column_distances.append(distance)  # Store the difference
    
    num_columns = len(test_row)  # Assumes both files have the same number of columns
    
    average_distances = []  # List to store the average distance for each column
    # Loop through each column index
    for i in range(num_columns):
        column_values = column_distances[i::num_columns]  # Extracts every nth value (n = number of columns)
        # Calculate the average distance for the column
        average_distance = sum(column_values) / len(column_values)
        average_distances.append(average_distance)  # Append the average distance to the list
    
    # Return the column names and the average distances
    return column_names, average_distances

# Main block to execute the functions
if __name__ == "__main__":
    if not PRO_DATA_PATH.exists():
        raise FileNotFoundError(
            "The expert reference data could not be found at:\n"
            f"{PRO_DATA_PATH}"
        )

    # Create the generated-data folder if it does not already exist.
    USER_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Record the user movement.
    record_pose_data(USER_DATA_PATH, 0.1, 3)

    # Compare the generated user data with the expert reference data.
    column_names, average_distances = calculate_file_score(
        USER_DATA_PATH,
        PRO_DATA_PATH
    )

    print("\nAverage Distance for Each Column:")

    for name, distance in zip(column_names, average_distances):
        print(f"{name}: {distance:.2f}")