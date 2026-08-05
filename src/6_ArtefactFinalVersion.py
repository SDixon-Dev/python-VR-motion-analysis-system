#imports the required modules and libraries
import tkinter as tk  # for GUI development
import triad_openvr  # for VR device interaction
import time  # for time-related functions
import sys  # for system-specific parameters and functions
import pandas as pd  # for data manipulation
import csv  # for reading and writing CSV files
from pathlib import Path

# Locate root folder of repo
PROJECT_ROOT =Path(__file__).resolve().parent.parent

# Define folders used to store for ref & generated data

SAMPLE_DATA_DIR = PROJECT_ROOT / "sample_data"
DATA_DIR = PROJECT_ROOT / "data"

# Define the full paths of the expert & user CSV files
PRO_DATA_PATH = SAMPLE_DATA_DIR / "ProData.csv"
USER_DATA_PATH = DATA_DIR / "USerData.csv"

# Function opens the screen to selecting a sport
def open_select_sport_screen():
    # Hide unnecessary buttons and shows the back button
    button_close.pack_forget()
    button_select_sport.pack_forget()
    button_back_sport.pack(side=tk.BOTTOM, pady=5)
    # Shows buttons for selecting a sport
    for sport_button in sport_buttons:
        sport_button.pack(pady=5)

# Function to open the screen for selecting a technique for a specific sport
def open_select_technique_screen(sport):
    global selected_sport  # Global variable to store the selected sport
    selected_sport = sport  # Set the selected sport
    # Updates label text and hides unnecessary buttons
    label.config(text="Select a technique for " + sport)
    button_back_sport.pack_forget()
    for sport_button in sport_buttons:
        sport_button.pack_forget()
    button_back_technique.pack(side=tk.BOTTOM, pady=5)  # Shows the back button
    # Shows buttons for technique selection
    for technique_button in technique_buttons[sport]:
        technique_button.pack(pady=5)

# Function to open the discipline's technique screen
def open_learn_technique_screen(technique):
    # Update the label text with the selected technique and sport
    label.config(text="Starting stance of " + technique + " in " + selected_sport)
    additional_text.config(text=additional_info[selected_sport][technique])  # Show additional information
    button_back_technique.pack_forget()  # Hide unnecessary buttons
    for technique_button in technique_buttons[selected_sport]:
        technique_button.pack_forget()
    additional_text.pack(side=tk.BOTTOM, pady=10)  # Show additional information text
    button_learn.pack(side=tk.BOTTOM, pady=5)  # Show the learn button

# Function to close the program
def close_program():
    root.destroy()  # Close the main window

# back Function to the main screen
def back_to_main_screen():
    # Reset the label text and hide unnecessary buttons
    label.config(text="Select an option")
    additional_text.pack_forget()
    button_back_sport.pack_forget()
    button_back_technique.pack_forget()
    button_learn.pack_forget()
    # Hide sport and technique selection buttons
    for sport_button in sport_buttons:
        sport_button.pack_forget()
    for technique_button in technique_buttons[selected_sport]:
        technique_button.pack_forget()
    # Shows main buttons
    button_close.pack(side=tk.BOTTOM, pady=5)
    button_select_sport.pack(side=tk.BOTTOM, pady=5)

# Function to run the learning process
def learn_technique():
    """Record a user movement and compare it with the expert movement."""

    if not PRO_DATA_PATH.exists():
        print(
            "The expert reference data could not be found at:\n"
            f"{PRO_DATA_PATH}"
        )
        return

    # Create the generated-data folder if it does not already exist.
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Record the user's movement and save it in the data folder.
    record_pose_data(USER_DATA_PATH, 0.1, 3)

    # Compare the user's recording with the expert reference recording.
    column_names, average_distances = calculate_file_score(
        USER_DATA_PATH,
        PRO_DATA_PATH
    )

    print("\nAverage Distance for Each Column:")

    for name, distance in zip(column_names, average_distances):
        print(f"{name}: {distance:.2f}")




# Function to record positional data of VR controllers and save it to a CSV file
def record_pose_data(file_path, interval, move_length):
    v = triad_openvr.triad_openvr()  # Initialize VR device
    v.print_discovered_objects()  # Print discovered VR objects

    data = []  # List to store positional data

    columns = ['x1', 'y1', 'z1','yaw1','pitch1','roll1','x2','y2','z2','yaw2','pitch2','roll2']
    posDf = pd.DataFrame(columns=columns)  # Convert data to DataFrame
    start_time = time.time()
    while True:
        start = time.time()
        txt = ""
        pose_data = {}
        controller_array = []
        # Loop through each VR controller device
        for device_name in ["controller_1", "controller_2"]:
            pose = v.devices[device_name].get_pose_euler()  # Get pose data
            controller_array += pose  # Appends data to array
            pose_data[device_name] = pose  # Stores the data in the dictionary
            for each in pose:
                txt += "%.4f" % each
                txt += " "
        print("\r" + txt, end="")
        data.append(pose_data)  # Append pose data to the main data list
        # Create a new row for the DataFrame with controller pose data
        new_controller_row = {"x1": controller_array[0], "y1": controller_array[1], "z1": controller_array[2], "yaw1": controller_array[3], "pitch1": controller_array[4], "roll1": controller_array[5],
                              "x2": controller_array[6], "y2": controller_array[7], "z2": controller_array[8], "yaw2": controller_array[9], "pitch2": controller_array[10], "roll2": controller_array[11]}
        posDf.loc[len(posDf)] = new_controller_row
        sleep_time = interval-(time.time()-start)
        if time.time() - start_time >= move_length:
            print("Move finished!")
            break
        if sleep_time > 0:
            time.sleep(sleep_time)

    # Convert the supplied file location into a Path object.
    file_path = Path(file_path)

    # Create the destination folder if it does not already exist.
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the recorded positional data to the supplied location.
    posDf.to_csv(file_path, index=False)


# Function to calculate the average distance between corresponding values in the two CSV files
def calculate_file_score(test_file, target_file):
    column_distances = []
    column_names = []
    
    with open(test_file, 'r') as test_f, open(target_file, 'r') as target_f:
        test_reader = csv.reader(test_f)
        target_reader = csv.reader(target_f)
        
        test_header = next(test_reader)  # Store header row
        target_header = next(target_reader)  # Skip header row
        
        for test_val, target_val in zip(test_header, target_header):
            column_names.append(test_val)
        
        for test_row, target_row in zip(test_reader, target_reader):
            for test_val, target_val in zip(test_row, target_row):
                test_val = float(test_val)
                target_val = float(target_val)
                distance = test_val - target_val  # Retain difference sign
                column_distances.append(distance)  # Store the difference
    
    num_columns = len(test_row)  # Assumes both files have the same number of columns
    
    average_distances = []
    for i in range(num_columns):
        column_values = column_distances[i::num_columns]  # Extracts every nth value (n = number of columns)
        average_distance = sum(column_values) / len(column_values)
        average_distances.append(average_distance)
    
    return column_names, average_distances

# Create the main window
root = tk.Tk()
root.title("Project GUI")
root.geometry("300x300")  # Set window size

# Create label to display screen content
label = tk.Label(root, text="Select an option")
label.pack(pady=5)

# Create additional label for extra information
additional_text = tk.Label(root, text="")
additional_text.pack(pady=5)

# Create buttons for Screen 1
button_close = tk.Button(root, text="Close Program", command=close_program)
button_close.pack(side=tk.BOTTOM, pady=5)

button_select_sport = tk.Button(root, text="Select Sport", command=open_select_sport_screen)
button_select_sport.pack(side=tk.BOTTOM, pady=5)

# Create buttons for Screen 2 (Select Sport)
button_back_sport = tk.Button(root, text="Back", command=back_to_main_screen)

# Create sport selection buttons
sport_buttons = []
sports = ["Fencing", "Kendo", "Iaido"]
for sport in sports:
    button = tk.Button(root, text=sport, command=lambda sport=sport: open_select_technique_screen(sport))
    sport_buttons.append(button)

# Create buttons for Screen 3 (Select Technique)
button_back_technique = tk.Button(root, text="Back", command=back_to_main_screen)

# Create technique selection buttons for each sport
technique_buttons = {
    "Fencing": [tk.Button(root, text="Lunge", command=lambda: open_learn_technique_screen("Lunge")),
                 tk.Button(root, text="Parry", command=lambda: open_learn_technique_screen("Parry")),
                 tk.Button(root, text="Feint", command=lambda: open_learn_technique_screen("Feint"))],
    "Kendo": [tk.Button(root, text="Kirikaeshi", command=lambda: open_learn_technique_screen("Kirikaeshi")),
                   tk.Button(root, text="Men-Uchi", command=lambda: open_learn_technique_screen("Men-Uchi")),
                   tk.Button(root, text="Tsuki", command=lambda: open_learn_technique_screen("Tsuki"))],
    "Iaido": [tk.Button(root, text="Nukitsuke", command=lambda: open_learn_technique_screen("Nukitsuke")),
               tk.Button(root, text="Kiritsuke", command=lambda: open_learn_technique_screen("Kiritsuke")),
               tk.Button(root, text="Chiburui", command=lambda: open_learn_technique_screen("Chiburui"))]
}

# Create buttons for Screen 4 (Learn Technique)
button_learn = tk.Button(root, text="Practice", command=learn_technique)

# Information about the sports techniques
additional_info = {
    "Fencing": {
        "Lunge": "Starting Stance:...",
        "Parry": "Starting Stance:...",
        "Feint": "Starting Stance:..."
    },
    "Kendo": {
        "Kirikaeshi": "Starting Stance:...",
        "Men-Uchi": "Starting Stance:...",
        "Tsuki": "Starting Stance:..."
    },
    "Iaido": {
        "Nukitsuke": "Starting Stance:...",
        "Kiritsuke": "Starting Stance:...",
        "Chiburui": "Starting Stance:..."
    }
}

# Runs the application
root.mainloop()