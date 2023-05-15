import cv2
import numpy as np
import matplotlib.pyplot as plt

# Set the backend to TkAgg
import matplotlib
matplotlib.use('TkAgg')

try:
    # Read the image
    img = cv2.imread('/home/pi/ndviphotos/image.jpg')

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding with adjusted parameters
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 5)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours by color range and area
    white_contours = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        roi = img[y:y+h, x:x+w]
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0, 0, 200], dtype=np.uint8)
        upper_white = np.array([180, 30, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv_roi, lower_white, upper_white)
        if cv2.contourArea(contour) > 50 and cv2.countNonZero(mask) > 0:
            white_contours.append(contour)

    # Draw rectangles around white contours
    for contour in white_contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the image using matplotlib
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

    # Count the number of white areas
    num_white_areas = len(white_contours)
    print('Number of white areas:', num_white_areas)

except Exception as e:
    print("An error occurred:", str(e))
