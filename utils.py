import csv
import pandas as pd

# Function to load data from a CSV file into a dictionary
def load_data_from_csv(filename):
    data_table = {}
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract relevant data
            for quality in ['8.8', '10.9', '12.9']:
                if quality not in data_table:
                    data_table[quality] = {}
                size_bolt = int(row['Size Nut [mm]'])
                # Store torque and tool names
                data_table[quality][size_bolt] = {
                    'Torque': row[f'{quality} Torque'],
                    'Tensioner': row[f'{quality} Tensioner'],
                    'Hydraulic Pneumatic Torque': row[f'{quality} Hydraulic Pneumatic Torque'],
                    'Hydraulic Electrical Torque': row[f'{quality} Hydraulic Electrical Torque'],
                    'Hydraulic Battery Torque': row[f'{quality} Hydraulic Battery Torque'],
                    'Rotary Screwdriver Pneumatic Torque': row[f'{quality} Rotatry Screwdriver Pneumatic Torque'],
                    'Rotary Screwdriver Electrical Torque': row[f'{quality} Rotatry Screwdriver Electrical Torque'],
                    'Rotary Screwdriver Battery Torque': row[f'{quality} Rotatry Screwdriver Battery Torque'],
                    'Pneumatic Tensioner': row[f'{quality} Pneumatic Tensioner'],
                    'Electrical Tensioner': row[f'{quality} Electrical Tensioner'],
                }
    return data_table

# Function to get quality
def get_user_input():
    quality = input("Choose Quality of bolt (8.8, 10.9, 12.9): ")
    return quality

# Function to choose between Torque or Tensioner
def choose_torque_or_tension():
    choice = input("Choose (1) Torque or (2) Tensioner: ").strip()
    return choice

# Function to choose between hydraulic or rotary screwdriver
def choose_tool_type():
    tool_type = input("Choose (1) Hydraulic or (2) Rotary screwdriver: ").strip()
    return tool_type

# Function to choose between pneumatic or electrical tensioner
def choose_tensioner_type():
    tensioner_type = input("Choose (1) Pneumatic Tensioner or (2) Electrical Tensioner: ").strip()
    return tensioner_type

# Function to choose tool subtype
def choose_tool_subtype(tool_type):
    if tool_type == '1':
        subtype = input("Choose (1) Pneumatic, (2) Electric, or (3) Battery operated tool: ").strip()
    elif tool_type == '2':
        subtype = input("Choose (1) Pneumatic, (2) Electric, or (3) Battery operated tool: ").strip()
    else:
        print("Invalid tool type selected.")
        return None
    return subtype
def convert_xlsx_to_csv(xlsx_file, csv_file):
    # Read the Excel file
    data_xls = pd.read_excel(xlsx_file, index_col=None)
    # Write to a CSV file
    data_xls.to_csv(csv_file, encoding='utf-8', index=False)

# Example usage
convert_xlsx_to_csv('ML_Data.xlsx', 'ML_Data.csv')

def round_to_nearest(input_number):
    df = pd.read_csv('ML_Data.csv')
    numbers = df['Size Nut [mm]'].tolist()
    
    # Find the correct bolt size to nearest value as provided by company
    nearest_number = min(numbers, key=lambda x: abs(x - input_number))
    
    return nearest_number


