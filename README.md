SLAM to Floor Plan Conversion
This project processes a SLAM (Simultaneous Localization and Mapping) generated image, detects walls and structural boundaries, and generates a simplified floor plan. The output is stored both as a PNG image and a JSON file containing the floor plan's line coordinates.

Features:
1. Image preprocessing to reduce noise (using Gaussian blur).
2. Edge detection using the Canny edge detection algorithm.
3. Line detection using Hough Line Transform.
4. Floor plan generation saved as both PNG and JSON.

Input:
A SLAM-generated image (typically a map image) of a room or building.

Output:
- A PNG image representing the floor plan with lines marking walls and boundaries.
- A JSON file containing the coordinates of the walls and boundaries detected in the image.

Prerequisites
Before running the code, make sure you have the following installed:

1. Python 3.x 
2. OpenCV for image processing
3. NumPy for numerical operations
4. JSON for saving the output in JSON format

You can install the required libraries using pip:
pip install opencv numpy


Project Structure

SLAM_TASK/
│
├── src/
│   ├── slam_task.py             # Main script for processing SLAM images
│
├── output/
│   ├── floor_plan_Image/       # Folder for saving the floor plan images (PNG)
│   ├── floor_plan_JSON/        # Folder for saving the floor plan data (JSON)
│
├── README.md                   # Documentation file (you are reading this!)

How to Run the Code

1. Run the script:
To run the script, pass the path of the SLAM image you want to process as a command-line argument. The script will generate a floor plan in both PNG and JSON formats.

python src/slam_task.py data/room1.pgm

2. Output files:
The script will generate:

- A floor plan image (PNG) saved to output/floor_plan_Image/room1.png (depending on the room name in the image path).
- A floor plan JSON saved to output/floor_plan_JSON/room1.json



