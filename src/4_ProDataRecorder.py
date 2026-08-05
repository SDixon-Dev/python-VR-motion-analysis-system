#imports the various modules and libraries required
import triad_openvr  # for accessing VR controller data
import time  # for time-related functions
import sys  # for system-related functions
import pandas as pd  # pandas library for data manipulation

def record_pose_data(file_path, interval, move_length):
    # Create a triad_openvr object to interact with VR devices
    v = triad_openvr.triad_openvr()
    # Prints discovered objects, such as VR controllers
    v.print_discovered_objects()

    data = []  # List to store positional data

    # Define the column names of the coordinates and Euler angles for the DataFrame to store positional data
    columns = ['x1', 'y1', 'z1','yaw1','pitch1','roll1','x2','y2','z2','yaw2','pitch2','roll2']
    # Creates an empty DataFrame with specified column names
    posDf = pd.DataFrame(columns=columns)
    # Start recording time
    start_time = time.time()
    # Loop continuously recording positional data until the defined move_length is reached
    while True:
        start = time.time()  # Record start time 
        txt = ""  # Initialize an empty string to store positional data
        pose_data = {}  # Initialize a dictionary to store pose data for each device
        controller_array = []  # Initialize an empty list to store pose data of both controllers
        # Loop through each VR controller device
        for device_name in ["controller_1", "controller_2"]:
            # Get the current pose (position and orientation) of the device in Euler angles format
            pose = v.devices[device_name].get_pose_euler()
            # Add pose data to controller_array list
            controller_array += pose
            # Add pose data to pose_data dictionary
            pose_data[device_name] = pose
            # Concatenate pose data into a string for display
            for each in pose:
                txt += "%.4f" % each  # Format pose data to 4 decimal places
                txt += " "
        # Display the concatenated pose data
        print("\r" + txt, end="")
        # Append the pose_data dictionary to the data list
        data.append(pose_data)
        # Create a new row for the DataFrame with the controller pose data
        new_controller_row = {"x1": controller_array[0], "y1": controller_array[1], "z1": controller_array[2], "yaw1": controller_array[3], "pitch1": controller_array[4], "roll1": controller_array[5],
                              "x2": controller_array[6], "y2": controller_array[7], "z2": controller_array[8], "yaw2": controller_array[9], "pitch2": controller_array[10], "roll2": controller_array[11]}
        # Append the new row to the DataFrame
        posDf.loc[len(posDf)] = new_controller_row
        # Calculate the time to sleep to maintain the specified interval between recordings
        sleep_time = interval-(time.time()-start)
        # Check if the move_length has been reached, if so, end the loop
        if time.time() - start_time >= move_length:
            print("Move finished!")
            break
        # If sleep_time is positive, sleep for that duration
        if sleep_time > 0:
            time.sleep(sleep_time)

    # Save the DataFrame to a CSV file
    posDf.to_csv(file_path, index=False)

if __name__ == "__main__":
    # Check if command line arguments are correct
    if len(sys.argv) < 4:
        print("Usage: python script.py <output_file_path> <interval> <move_length>")
        sys.exit(1)

    # Extracts the command line arguments: output file path, recording interval, and move length
    output_file = sys.argv[1]
    interval = float(sys.argv[2])
    move_length = float(sys.argv[3])

    # Call the record_pose_data function with the provided arguments
    record_pose_data(output_file, interval, move_length)