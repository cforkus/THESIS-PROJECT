import picamera
import time
import os
import subprocess

#initialize the camera
camera = picamera.PiCamera()

#set the resolution of camera
camera.resolution = (640, 480)

#set filename for the image
filename = 'image'

# specify the destination directory
destination = "/home/pi/ndviphotos/{}.jpg".format(filename)

try:
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

# check if feh is installed, and install it if not
feh_check = subprocess.run(['which', 'feh'], capture_output=True, text=True)
if feh_check.returncode != 0:
   print('feh is not installed, installing...')
   subprocess.run(['sudo', 'apt-get', 'update'])
   subprocess.run(['sudo', 'apt-get', 'install', '-y', 'feh'])
   print('feh installation complete')

#open in default image viewer
os.system('feh ' + destination)

except KeyboardInterrupt:
    # If user interrupts the program with Ctrl+C
    print('\nProgram interrupted by user')
except Exception as e:
    # If an error occurs
    print('An error occurred:', str(e))

finally:
    # always close the camera, even if an error occurred
    camera.close()
