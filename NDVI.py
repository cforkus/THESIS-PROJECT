import cv2
from time import strftime
import numpy as np
import os
import RPi.GPIO as GPIO

# Define paths
photo_path = "/home/pi/ndviphotos/"
timestamp = strftime("%d:%m:%y:%I:%M:%S:%p")
noir_path = "{}{}.jpg".format(photo_path, timestamp + "Noir")
rbg_path = "{}{}.jpg".format(photo_path, timestamp + "RBG")
ndvi_path = "{}{}.jpg".format(photo_path, timestamp + "ndvi")

# Set GPIO pin outputs
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT)

# Take Noir photo
GPIO.output(7, GPIO.LOW)
os.system("raspistill -o {}".format(noir_path))

# Take RBG photo
GPIO.output(7, GPIO.HIGH)
os.system("raspistill -o {}".format(rbg_path))

# Increase brightness and contrast of Noir photo
convert_command = "convert -brightness-contrast -20x30 {} {}".format(noir_path, noir_path)
os.system(convert_command)

# Convert Noir and RBG photos into arrays
with cv2.imread(noir_path) as image:
    image = np.array(image, dtype=float) / float(255)
with cv2.imread(rbg_path) as image2:
    image2 = np.array(image2, dtype=float) / float(255)

# Get NIR values from Noir photo
def get_nir(image):
    if image.ndim == 3:
        b, g, r = cv2.split(image)
        nir = r.astype(float)
    elif image.ndim == 2:
        nir = image.astype(float)
    return nir

# Get red value from RBG photo
def get_red(image2):
    b, g, r, = cv2.split(image2)
    red = r.astype(float)
    return red

# Calculate NDVI and save output
def ndvi(image, image2):
    bottom = (get_nir(image) + get_red(image2))
    bottom[bottom == 0] = 0.01
    ndvi = (get_nir(image) - get_red(image2)) / bottom
    ndvi = np.multiply(ndvi, 1000)
    cv2.imwrite(ndvi_path, ndvi)

ndvi(image, image2)

