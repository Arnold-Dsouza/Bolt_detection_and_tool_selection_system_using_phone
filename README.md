# Research and Development Project 2025
## Bolt Detection and Tool Selection System

## **Overview**
This project is designed to detect bolts in an image, calculate their size, and recommend appropriate tools (torque or tensioner) based on the bolt's size and quality. The system uses YOLOv11 (You Only Look Once) for bolt detection, ArUco markers for size calibration, and a CSV-based data table for tool selection.

## **Features**
- **Bolt Detection**: Uses YOLO v11 model to detect bolts in an image.
- **Size Calculation**: Utilizes ArUco markers to calculate the bolt size in millimeters.
- **Tool Selection**: Recommends tools (torque or tensioner) based on bolt size and quality.
- **Camera Calibration**: Includes a calibration module to ensure accurate size measurements.

## **Requirements**
The project requires the following Python packages:
- **Roboflow**: For YOLOv11 model inference.
- **OpenCV**: For image processing and ArUco marker detection.
- **NumPy**: For numerical operations.
- **Pandas**: For handling CSV data.
- **Other dependencies**: Listed in `requirements.txt`.

## **Installation**
1. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```
2. **Set up Roboflow**:
   - Log in to Roboflow and obtain your API key.
   - Update the `roboflow.login()` function in `tool_selector.py` with your API key.

## **Usage**
1. **Camera Calibration**:
   - Place the Charuco board in front of the camera and capture multiple images.
   - Run the calibration script:
     ```bash
     python3 calibration/calibration.py
     ```
   - This will generate `camera_matrix.npy` and `dist_coeffs.npy` files.

2. **Bolt Detection and Tool Selection**:
   - Take the images of bolt with ArUco marker in the camera's field of view.
   - Place them inside `test_img` folder
   - Run the tool selection script, after specifying the image path:
     ```bash
     python3 Bolt_detection/tool_selector.py
     ```
   - The script will:
     - Detect the bolt and calculate its size.
     - Prompt the user to select the bolt quality and tool type.
     - Recommend the appropriate tool based on the input.

## **File Structure**
- **Bolt_detection/**
  - `utils.py`: Contains utility functions for loading data, user input, and tool selection.
  - `tool_selector.py`: Main script for bolt detection and tool selection.
  - `requirements.txt`: Lists all required Python packages.
- **calibration/**
  - `calibration.py`: Script for camera calibration using Charuco board.
  - `images/`: Directory for storing calibration images.
  - `calib_mat/`: Directory for storing calibration matrices.

## **Data Table**
The tool selection is based on a CSV file provided by Plarad GmBh company (`ML_Data.csv`) that contains the following columns:
- **Size Nut [mm]**: Bolt size in millimeters.
- **8.8 Torque**, **10.9 Torque**, **12.9 Torque**: Torque values for different bolt qualities.
- **8.8 Tensioner**, **10.9 Tensioner**, **12.9 Tensioner**: Tensioner values for different bolt qualities.
- **Hydraulic Pneumatic Torque**, **Hydraulic Electrical Torque**, **Hydraulic Battery Torque**: Torque values for hydraulic tools.
- **Rotary Screwdriver Pneumatic Torque**, **Rotary Screwdriver Electrical Torque**, **Rotary Screwdriver Battery Torque**: Torque values for rotary screwdrivers.
- **Pneumatic Tensioner**, **Electrical Tensioner**: Tensioner values for pneumatic and electrical tools.

## **Limitations**
- The system relies on the presence of an ArUco marker for accurate size calculation.
- At present, the tool selection is based on predefined data in the CSV file, which has to be updated for new tools or bolt qualities.

## **Future Work**
- **Expand Data Table**: Include more bolt sizes and qualities in the CSV file.
- **Improve Detection**: Enhance the YOLO model to make it robust so as to detect bolts without the need for ArUco markers.
- **User  Interface**: (in progress) Developing a smartphone application for easier interaction with the system.


## **Contact**
For any inquiries or issues, please contact:
- **Arnold Dsouza**: arnold.dsouza@smail.inf.h-brs.de
