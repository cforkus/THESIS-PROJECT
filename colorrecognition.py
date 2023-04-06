# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 21:23:45 2023

@author: cfork
"""

import cv2

#read the image
img = cv2.imread('image.jpg')

#convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#threshold the image to create a binary mask
thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)[1]

#find contours in the mask
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#iterate over each contour and draw rectangle around it
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w > 10 and h > 10: #filter out small contours
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
#display the image
cv2.imshow('Result', img)
cv2.waitKey(0)

#count the number of contours that correspond to white areas
num_white_areas = 0
for contour in contours:
    if cv2.contourArea(contour) > 50: #change the threshold area as per requirement
        num_white_areas += 1
        
#print the number of white areas
print('Number of white areas:', num_white_areas)