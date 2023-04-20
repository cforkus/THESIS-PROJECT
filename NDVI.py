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
image = cv2.imread(noir_path)
image = np.array(image, dtype=float) / float(255)
image2 = cv2.imread(rbg_path)
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
    b, g, r = cv2.split(image2)
    red = r.astype(float)
    return red

# Calculate NDVI and save output
def ndvi(image, image2):
    bottom = (get_nir(image) + get_red(image2))
    bottom[bottom == 0] = 0.01
    ndvi_result = (get_nir(image) - get_red(image2)) / bottom
    ndvi_result = np.multiply(ndvi_result, 1000)

    # Get min and max values of NDVI image
    ndvi_min = np.amin(ndvi_result)
    ndvi_max = np.amax(ndvi_result)

    # Convert NDVI image to uint8
    ndvi_result = (255 * (ndvi_result - ndvi_min) / (ndvi_max - ndvi_min)).astype(np.uint8)

    # Apply a color map to the NDVI image
    ndvi_color = cv2.applyColorMap(ndvi_result, cv2.COLORMAP_JET)

    # Add text with NDVI value to the NDVI image
    ndvi_text = "NDVI: {:.2f}".format(np.mean(ndvi_result))
    cv2.putText(ndvi_color, ndvi_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Save NDVI image
    cv2.imwrite(ndvi_path, ndvi_color)

ndvi(image, image2)
