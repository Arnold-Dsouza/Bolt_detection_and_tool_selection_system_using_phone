import cv2
import os
import numpy as np

def calibrate_camera_charuco(vertical_squares, horizontal_squares, square_length, marker_length, image_dir, output_dir):

    if not os.path.exists(image_dir):
        raise FileNotFoundError(f"Image directory '{image_dir}' does not exist.")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the Charuco board
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    charuco_board = cv2.aruco.CharucoBoard((horizontal_squares, vertical_squares), square_length, marker_length, aruco_dict)
    detector_params = cv2.aruco.DetectorParameters()

    # Collect all image file paths
    image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith((".jpg", ".png"))]
    if not image_files:
        raise ValueError("No images found in the specified directory.")

    all_corners = []
    all_ids = []
    image_size = None

    # Process each image
    for image_file in image_files:
        image = cv2.imread(image_file)
        if image is None:
            print(f"Warning: Unable to read image '{image_file}'. Skipping.")
            continue

        if image_size is None:
            image_size = (image.shape[1], image.shape[0])  # (width, height)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=detector_params)

        if marker_ids is not None and len(marker_ids) > 0:
            retval, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(
                marker_corners, marker_ids, gray, charuco_board
            )
            if retval:
                all_corners.append(charuco_corners)
                # print(all_corners.shape)
                all_ids.append(charuco_ids)

    # Ensure there are enough valid images
    if len(all_corners) < 3:
        raise ValueError("Not enough valid images with detected Charuco corners for calibration.")

    # Perform calibration
    retval, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(all_corners, all_ids, charuco_board, image_size, None, None)

    if not retval:
        raise RuntimeError("Camera calibration failed.")

    # Save calibration parameters
    camera_matrix_file = os.path.join(output_dir, "camera_matrix.npy")
    dist_coeffs_file = os.path.join(output_dir, "dist_coeffs.npy")

    np.save(camera_matrix_file, camera_matrix)
    np.save(dist_coeffs_file, dist_coeffs)

    print(f"Reprojection error: {retval}")
    print(f"Calibration successful!")
    print(f"Camera matrix saved to: {camera_matrix_file}")
    print(f"Distortion coefficients saved to: {dist_coeffs_file}")

    return camera_matrix_file, dist_coeffs_file


if __name__ == "__main__":
    
    # Configuration of our setup
    VERTICAL_SQUARES = 7
    HORIZONTAL_SQUARES = 5
    SQUARE_LENGTH = 0.037  # In meters
    MARKER_LENGTH = 0.022  # In meters
    IMAGE_DIR = "./calibration/images"
    OUTPUT_DIR = "./calibration/calib_mat"

    # Calibrate camera
    calibrate_camera_charuco(VERTICAL_SQUARES, HORIZONTAL_SQUARES, SQUARE_LENGTH, MARKER_LENGTH, IMAGE_DIR, OUTPUT_DIR)

# camera_matrix_path = os.path.join(OUTPUT_DIR, "camera_matrix.npy")
# print(np.load(camera_matrix_path))
