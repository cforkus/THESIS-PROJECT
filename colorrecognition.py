import cv2
import numpy as np
import matplotlib.pyplot as plt

# Set the backend to TkAgg
import matplotlib
matplotlib.use('TkAgg')

try:
    #read the image
    img = cv2.imread('/home/pi/ndviphotos/image.jpg')

    #convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
    # Iterate over each contour and draw a rectangle around it
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 10 and h > 10:  # Filter out small contours
            # Calculate the extent of the contour (ratio of contour area to bounding rectangle area)
            extent = cv2.contourArea(contour) / (w * h)
            if extent < 0.9:  # Filter out contours with high extent (likely glare)
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    #display the image using matplotlib
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off') # remove axis and ticks
    plt.show()

    #count the number of contours that correspond to white areas
    num_white_areas = 0
    for contour in contours:
        if cv2.contourArea(contour) > 50: #change the threshold area as per requirement
            num_white_areas += 1

    #print the number of white areas
    print('Number of white areas:', num_white_areas)

except Exception as e:
    print("An error occurred:", str(e))

