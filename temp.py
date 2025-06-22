import cv2
import numpy as np

image = cv2.imread('character1_0.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh_value, img_thresh = cv2.threshold(gray, 177, 255, cv2.THRESH_BINARY)
img_denoised = cv2.fastNlMeansDenoising(img_thresh, None, 70, 7, 21) 
kernel = np.ones((1, 20), np.uint8)
img_dilated = cv2.morphologyEx(img_denoised, cv2.MORPH_CLOSE, kernel)

#cv2.imshow("Original Image", image)
#cv2.imshow("grayscaled Image", img_thresh)
#cv2.imshow("grayscaled&denoised Image", img_denoised)
cv2.imshow("small gaps filled Image", img_dilated)
# Wait for a key press before closing the window
cv2.waitKey(0)
cv2.destroyAllWindows()

# contours, hierachy = cv2.findContours(img_denoised, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# x, y, w, h = cv2.boundingRect(hierachy)
# cv2.rectangle(img_denoised, (x, y), (x+w, y+h), (255, 0, 0), 2)