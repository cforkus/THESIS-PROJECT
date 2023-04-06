import picamera
import time
import os

#initialize the camera
camera = picamera.PiCamera()

#set the resolution of camera
camera.resolution = (640, 480)

#set filename for the image
filename = 'image'

# specify the destination directory
destination = "/home/pi/ndviphotos/{}.jpg".format(filename)

# wait for a key press to capture the image
input('Press Enter to capture the image...')

#capture the image
camera.capture(destination)

# print a message that image has been captures
print('image captured successfully!')

#wait for 2 seconds before exiting
time.sleep(2)

#close the camera
camera.close()

#open in default image viewer
os.system('feh ' + destination)

