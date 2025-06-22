import cv2
import numpy as np

# Input image path
image_path = 'character2_0.jpg'

# Load the image in grayscale
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh_value, img_thresh = cv2.threshold(gray, 177, 255, cv2.THRESH_BINARY)

# Remove noise of the image
img_denoised = cv2.fastNlMeansDenoising(img_thresh, None, 50, 7, 21) 

# Dilate the gaps (mostly horizontally) -> contour can be easily detected
kernel = np.ones((4,40), np.uint8)
img_dilated = cv2.morphologyEx(img_denoised, cv2.MORPH_CLOSE, kernel)

# Show image, wait for a key press before closing the window
#cv2.imshow("Grayscaled Image", img_denoised)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Output the image
output_path='character2_1.jpg'
cv2.imwrite(output_path, img_denoised)

def detect_character_boxes(image_a, min_area=0, max_area=15000):
    # Find contours of the characters
    contours, _ = cv2.findContours(image_a, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    filtered_contours = [contour for contour in contours if min_area < cv2.contourArea(contour) < max_area]

    boxes = []
    for contour in filtered_contours:
        x, y, w, h = cv2.boundingRect(contour)
        # Filter small noise
        if w > 30 and h > 30:
            boxes.append([x, y, w, h])

    return boxes

# Function to draw the bounding boxes on the image
def draw_boxes(image_b, boxes, output_path_2='character2_2.jpg'):
    for (x, y, w, h) in boxes:
        cv2.rectangle(image_b, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.imwrite(output_path_2, image_b)
    #cv2.imshow("contour", image_b)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

generatedboxes = detect_character_boxes(img_dilated)
img_boxed = draw_boxes(img_denoised, generatedboxes)

# Print the results
for i, (x, y, w, h) in enumerate(generatedboxes, start=1):
   print(f"Char {i}: x={x}, y={y}, width={w}, height={h}")