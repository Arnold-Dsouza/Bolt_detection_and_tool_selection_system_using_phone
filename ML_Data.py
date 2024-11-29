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
                size_bolt = int(row['Size Bolt [mm]'])
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

# Function to get user input for size and quality
def get_user_input():
    size = int(input("Enter Size of Bolt (e.g., 14): "))
    quality = input("Choose Quality of bolt (8.8, 10.9, 12.9): ")
    return size, quality

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
convert_xlsx_to_csv('../ML_Data.xlsx', 'ML_Data.csv')

# Main function to run the program
def main():
    # Load data from CSV file
    data_table = load_data_from_csv('ML_Data.csv')
    
    size, quality = get_user_input()
    
    # Check if the combination exists in the data table
    if quality in data_table and size in data_table[quality]:
        print(f"Selected Size: {size}, Quality: {quality}")
        
        # Get Torque or Tensioner choice
        choice = choose_torque_or_tension()
        
        if choice in ['1', '2']:
            value_key = 'Torque' if choice == '1' else 'Tensioner'
            value = data_table[quality][size][value_key]
            print(f"The value corresponding to {value_key} is: {value}")
            
            if choice == '1':  # Torque selected
                # Choose between hydraulic or rotary screwdriver
                tool_type = choose_tool_type()
                
                if tool_type in ['1', '2']:
                    subtype = choose_tool_subtype(tool_type)
                    if subtype:
                        # Determine which torque value to output based on user selection
                        if tool_type == '1':  # Hydraulic
                            if subtype == '1':
                                tool_name = data_table[quality][size]['Hydraulic Pneumatic Torque']
                            elif subtype == '2':
                                tool_name = data_table[quality][size]['Hydraulic Electrical Torque']
                            elif subtype == '3':
                                tool_name = data_table[quality][size]['Hydraulic Battery Torque']
                            else:
                                print("Invalid subtype selected.")
                                return
                        else:  # Rotary
                            if subtype == '1':
                                tool_name = data_table[quality][size]['Rotary Screwdriver Pneumatic Torque']
                            elif subtype == '2':
                                tool_name = data_table[quality][size]['Rotary Screwdriver Electrical Torque']
                            elif subtype == '3':
                                tool_name = data_table[quality][size]['Rotary Screwdriver Battery Torque']
                            else:
                                print("Invalid subtype selected.")
                                return
                        # Check for NaN or unavailable tools
                        if tool_name == '#N/A' or not tool_name:
                            print("No tool available for this configuration.")
                        else:
                            print(f"You have selected Tool: {tool_name}")
                    else:
                        print("No valid subtype selected.")
                else:
                    print("Invalid tool type selected.")
            elif choice == '2':  # Tensioner selected
                tensioner_type = choose_tensioner_type()
                
                if tensioner_type in ['1', '2']:
                    if tensioner_type == '1':
                        tensioner_value = data_table[quality][size].get('Pneumatic Tensioner', "No tool available")
                    elif tensioner_type == '2':
                        tensioner_value = data_table[quality][size].get('Electrical Tensioner', "No tool available")
                else:
                    print("Invalid tensioner type selected.")
                # Check for NaN or unavailable tools
                if tensioner_value == '#N/A' or not tensioner_value:
                    print("No tool available for this configuration.")
                else:
                    print(f"You have selected Tool: {tensioner_value}")
        

# Run the program
if __name__ == "__main__":
    main()
