import cv2
import numpy as np
import sys
import json
import os


# to read slam generated images
def read_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")
    
    #resize the image if required 
    img = cv2.resize(img, (850, 650))
    print("image read done", img.shape)

    #to see the image
    # cv2.imshow("Original Image", img)
    # cv2.waitKey(0)
    return img

#preprocess image - smoothing to remove noices
def pre_process_image(image):

    #using gaussian 
    blurred_image = cv2.GaussianBlur(image, (15,15), 0)
    print("blurring is done")

    #to see image
    # cv2.imshow("Blurred Image", blurred_image)
    # cv2.waitKey(0)
    return blurred_image


#detect edges using canny 
def detect_image_edges(image):

    edge_image = cv2.Canny(image, 1450, 1500, apertureSize= 5)
   
    #apply dilate to make edges solid
    kernel = np.ones((3,3), np.uint8)
    edges_dilated = cv2.dilate(edge_image, kernel, iterations=1)
    print("edge detection done")
    # cv2.imshow('edge detection', edges_dilated)
    # cv2.waitKey(0)
    # exit()
    return edges_dilated

def detect_image_lines(image, img):
    
    lines = cv2.HoughLinesP(image, 1, np.pi/180, 50, minLineLength=10, maxLineGap=1)
    
    # create blank image of same size
    blank_image = np.zeros_like(img)

    #draw lines based on hough transform to check 
    for line in lines:
        for x1, y1, x2, y2 in line:

            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
            cv2.line(blank_image,(x1,y1),(x2,y2),(255,255,255),2)
    
    print("line detection is done")
    # cv2.imshow('line_image', img)
    # cv2.imshow('line_blank', blank_image)
    # cv2.waitKey(0)
    return lines

def clean_up_image_lines(lines, img):

    #create empty image of same size
    cleaned_img = np.zeros_like(img, dtype=np.uint8)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(cleaned_img, (x1, y1), (x2, y2), 255, 1)  # Thicker walls
    
    # Apply dilation to make lines more solid
    kernel = np.ones((3, 3), np.uint8)
    cleaned_img = cv2.dilate(cleaned_img, kernel, iterations=1)
    print("clean up of lines completed")
    # cv2.imshow("Cleaned Lines", cleaned_img)
    # cv2.waitKey(0)
    
    return cleaned_img

# to save the floor plan as JSON
def save_as_json(lines, img, output_path_json):

    if lines is None:
        print("No lines detected, skipping JSON save.")
        return
    
    # create folder directory
    os.makedirs(os.path.dirname(output_path_json), exist_ok=True) 

    img_shape = img.shape

    # Convert lines to a dictionary format
    floor_plan_data = {
        "image_size": list(img_shape),
        "lines": [{"x1": int(x1), "y1": int(y1), "x2": int(x2), "y2": int(y2)} for x1, y1, x2, y2 in lines[:, 0]]
    }

    with open(output_path_json, 'w') as f:
        json.dump(floor_plan_data, f, indent=4)

    print(f"Saved floor plan as {output_path_json}")

# Function to save the floor plan as PNG
def save_floor_plan_as_image(floor_plan, output_path):
    cv2.imwrite(output_path, floor_plan)
    print(f"Saved floor plan as {output_path}")


def slam_to_floor_png(image_path):

    # Extract room name from input file name to use for JSON naming
    room_name = os.path.splitext(os.path.basename(image_path))[0]  # Remove extension
    output_path_json = f"output/floor_plan_JSON/{room_name}.json"
    output_path_floor_plan = f'output/floor_plan_Image/{room_name}.png'

    img = read_image(image_path)
    pre_processed_img = pre_process_image(img)
    image_with_edges = detect_image_edges(pre_processed_img)
    image_with_lines = detect_image_lines(image_with_edges, img)
    clean_image = clean_up_image_lines(image_with_lines, img)
    save_line_details = save_as_json(image_with_lines, img, output_path_json)
    save_floor_plan_image = save_floor_plan_as_image(clean_image, output_path_floor_plan)
    return image_with_lines


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("use: python slam_task.py <input image path>")
    else:
        input_image_path = sys.argv[1]
        slam_to_floor_png(input_image_path)