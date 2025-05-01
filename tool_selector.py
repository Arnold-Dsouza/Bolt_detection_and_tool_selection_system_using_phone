import roboflow
import cv2
from utils import *
import numpy as np

# Logging to Roboflow for model YOLO v11
roboflow.login()
rf = roboflow.Roboflow()

project = rf.workspace("boltv12").project("boltv2_yolo")
model   = project.version(3).model

# Load the camera matrix, distortion coefficients generated after calibration
camera_matrix = np.load("./calibration/calib_mat/camera_matrix.npy")
dist_coeffs= np.load("./calibration/calib_mat/dist_coeffs.npy")

# initializing the ArUco dictionary and detector 
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters =  cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

img_path = "./test_img/test_1.jpg"          # test image

prediction= model.predict(img_path, confidence=50, overlap=50)

img = cv2.imread(img_path)

# detect ArUco markers
corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)

if corners:
    int_corners = np.int0(corners)
    cv2.polylines(img, int_corners, True, (0, 255, 0), 2)

    # convert pixel to centimeter 
    aruco_perimeter = cv2.arcLength(corners[0], True) 
    pixel_cm_ratio = aruco_perimeter / 2.5
    pixel_mm_ratio = pixel_cm_ratio / 10

    # Processing YOLO predictions
    if not prediction:
        print("No more predictions")
        cv2.putText(img, "Bolt not detected, please try again", (100, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    else:
        for pred in prediction:
            x, y, width, height = pred['x'], pred['y'], pred['width'], pred['height']

            # Convert to pixel coordinates
            x_min = int(x - width / 2)
            y_min = int(y - height / 2)
            x_max = int(x + width / 2)
            y_max = int(y + height / 2)

            # Calculate bolt size
            object_width = width / pixel_mm_ratio
            object_height = height / pixel_mm_ratio
            min_dimension = min(object_width, object_height)

            # Draw bounding box
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

            # Add bolt size text
            cv2.putText(img, "Bolt Size: {} mm".format(round(min_dimension, 1)), (int(x - 150), int(y - 200)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

            print(f"Bounding box: ({x_min}, {y_min}, {x_max}, {y_max})")

            if len(corners) > 0:
                rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.025, camera_matrix, dist_coeffs)
                distance = np.linalg.norm(tvec)
            
            size= round_to_nearest(min_dimension)
            print(f"Diameter of bolt head: {size}")

            # Tool selector menu code starts here
            data_table = load_data_from_csv('ML_Data.csv')
            quality = get_user_input()

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
                                        continue
                                else:  # Rotary
                                    
                                    if subtype == '1':
                                        tool_name = data_table[quality][size]['Rotary Screwdriver Pneumatic Torque']
                                    elif subtype == '2':
                                        tool_name = data_table[quality][size]['Rotary Screwdriver Electrical Torque']
                                    elif subtype == '3':
                                        tool_name = data_table[quality][size]['Rotary Screwdriver Battery Torque']
                                    else:
                                        print("Invalid subtype selected.")
                                        continue
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

else:
    print("No ArUco markers detected. Unable to calculate bolt size.")

# saving the predicted image with the bolt size
cv2.imwrite("./test_result/result_4.jpg", img)
