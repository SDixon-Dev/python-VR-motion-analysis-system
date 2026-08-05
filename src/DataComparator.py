import csv

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
                distance = test_val - target_val  # Retain the sign of the difference
                column_distances.append(distance)  # Store the difference
    
    num_columns = len(test_row)  # Assuming both files have the same number of columns
    
    average_distances = []
    for i in range(num_columns):
        column_values = column_distances[i::num_columns]  # Extract every nth value where n is the number of columns
        average_distance = sum(column_values) / len(column_values)
        average_distances.append(average_distance)
    
    return column_names, average_distances

# Example usage:
test_file = "UserData.csv"
target_file = "ProData.csv"
column_names, average_distances = calculate_file_score(test_file, target_file)
print("Average Distance for Each Column:")
for name, distance in zip(column_names, average_distances):
    print(f"{name}: {distance:.2f}")