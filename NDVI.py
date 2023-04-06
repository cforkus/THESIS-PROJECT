# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
@author: corinforkus
"""

import cv2
from time import strftime
import numpy as np
import os
import RPi.GPIO as GPIO

timestamp = strftime("%d:%m:%y:%I:%M:%S:%p")

# Set GPIO pin outputs

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(7,GPIO.OUT)

# Get Noir and RBG images

# Take Noir
GPIO. output(7,GPIO.LOW)
os.system('raspistill -o /home/pi/thesis_prototype/python_testing/ndvi_photos/{}.jpg'. format(timestamp + "NOIR"))

# Take RBG
GPIO. output(7,GPIO.HIGH)
os.system('raspistill -o /home/pi/thesis_prototype/python_testing/ndvi_photos/{}.jpg'. format(timestamp + "RBG"))

image_path_Noir = ("/home/pi/thesis_prototype/python_testing/ndvi_photos/{}.jpg").format(timestamp + "Noir")
image_path_RBG = ("/home/pi/thesis_prototype/python_testing/ndvi_photos/{}.jpg").format(timestamp + "RBG")

#increase brightness and contrast of image
string_convert = ("convert -brightness-contrast -20x30" + "" + image_path_Noir + "" + image_path_Noir)
os.system(string_convert)

#convert Noir photo into array
image = cv2.imread(image_path_Noir)
image = np.array(image,dtype=float)/float(255)

#convert RBG photo into array
image2 = cv2.imread(image_path_RBG)
image2 = np.array(image2,dtype=float)/float(255)

#get NIR values from Noir photo
def get_nir(image):
    b, g, r, = cv2.split(image)
    nir = r.astype(float)
    return nir

#print(get_nir(image))
#cv2.imwrite('/home/pi/thesis_prototype/python_testing/ndvi_photos/{}.jpg").format(timestamp + "Noir_red"), get_nir(image))

#get red value from RBG
def get_red(image2):
    b, g, r, = cv2.split(image2)
    red = r.astype(float)
    return red

#print(get_red(image2))
#cv2.imwrite('/home/pi/thesis_prototype/python_testing/ndvi_photos/{}.jpg").format(timestamp + "RBG_red"), get_red(image2))

def ndvi(image, image2):
    bottom = (get_nir(image) + get_red(image2))
    bottom[bottom==0] = 0.01
    ndvi = (get_nir(image) - get_red(image2)) / bottom
    ndvi = np.multiply(ndvi, 1000)
    return ndvi

cv2.imwrite('/home/pi/thesis_prototype/python_testing/ndvi_photos/{}.jpg'.format(timestamp + "ndvi"), ndvi(image, image2))
