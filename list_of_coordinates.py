import cv2
import numpy as np
import pandas as pd

# Input image path
idx = 9
image_path = f"./character{idx}/character{idx}_0.jpg"

# Load the image in grayscale
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh_value, img_thresh = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY)

# Remove noise of the image
img_denoised = cv2.fastNlMeansDenoising(img_thresh, None, 15, 7, 21) 

#OPTIONAL!!!!! To remove the vertical lines
kernel_1 = np.ones((6,0), np.uint8)
img_eroded = cv2.erode(img_denoised, kernel_1, iterations=1)
img_denoised = cv2.dilate(img_eroded, kernel_1, iterations=1)

# Output the image
output_path=f"./character{idx}/character{idx}_1.jpg"
cv2.imwrite(output_path, img_denoised)

# Dilate the gaps (mostly horizontally) -> contour can be easily detected
kernel_2 = np.ones((10,30), np.uint8)
img_dilated = cv2.morphologyEx(img_denoised, cv2.MORPH_CLOSE, kernel_2)

# Show image, wait for a key press before closing the window
# cv2.imshow("Grayscaled Image", img_dilated)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


def detect_character_boxes(image_a, min_area=0, max_area=20000):
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
def draw_boxes(image_b, boxes, output_path_2=f"./character{idx}/character{idx}_2.jpg"):
    for (x, y, w, h) in boxes:
        cv2.rectangle(image_b, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.imwrite(output_path_2, image_b)
    #cv2.imshow("contour", image_b)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

generatedboxes = detect_character_boxes(img_dilated)
img_boxed = draw_boxes(img_denoised, generatedboxes)

# Prepare the data for Excel output
coordinates = []
for i, (x, y, w, h) in enumerate(generatedboxes, start=1):
    coordinates.append([i, x, y, w, h])

# Create a DataFrame from the data
listofcoordinates = pd.DataFrame(coordinates, columns=["No.", "X", "Y", "Width", "Height"])

# Arranging orders
listofcoordinates = listofcoordinates.sort_values('X', ascending=False).reset_index(drop=True)
listofcoordinates['Xi'] = ""
listofcoordinates.at[0,'Xi'] = 1
# If the current X value - previous X value >80, then recognize it as a new column
for i in range(1, len(listofcoordinates)):
    if listofcoordinates.loc[i - 1, 'X'] - listofcoordinates.loc[i, 'X'] < 100:
        listofcoordinates.at[i, 'Xi'] = listofcoordinates.at[i - 1, 'Xi']
    else:
        listofcoordinates.at[i, 'Xi'] = listofcoordinates.at[i - 1, 'Xi'] + 1
        
listofcoordinates = listofcoordinates.sort_values(['Xi','Y'],ascending=[True, True]).reset_index(drop=True)
listofcoordinates = listofcoordinates.drop('Xi', axis=1)

# Save the DataFrame to Excel
excel_output_path = f"./character{idx}/character{idx}_boxes_location.xlsx"
listofcoordinates.to_excel(excel_output_path, index=False, engine="openpyxl")
print(f"Bounding boxes saved to {excel_output_path}")