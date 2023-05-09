import picamera
import time
import os
import subprocess
import cv2

# Initialize the camera
camera = picamera.PiCamera()

# Disable camera effects and image processing
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0
camera.awb_mode = 'off'
camera.exposure_mode = 'auto'
# Set the resolution of the camera
camera.resolution = (640, 480)

# Set filename for the image
filename = 'image'

# Specify the destination directory
destination = "/home/pi/ndviphotos/{}.raw".format(filename)

try:
    # Wait for a key press to capture the image
    input('Press Enter to capture the image...')

    # Capture the raw Bayer image
    camera.capture(destination, format='raw')

    # Print a message that the image has been captured
    print('Image captured successfully!')

    # Perform demosaicing to obtain a full-color image
    raw_image = cv2.imread(destination, cv2.IMREAD_UNCHANGED)
    color_image = cv2.cvtColor(raw_image, cv2.COLOR_BayerRG2RGB)

    # Specify the output filename for the color image
    color_image_destination = "/home/pi/ndviphotos/{}.jpg".format(filename)

    # Save the demosaiced color image
    cv2.imwrite(color_image_destination, color_image)

    # Check if feh is installed, and install it if not
    feh_check = subprocess.run(['which', 'feh'], capture_output=True, text=True)
    if feh_check.returncode != 0:
        print('feh is not installed, installing...')
        subprocess.run(['sudo', 'apt-get', 'update'])
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'feh'])
        print('feh installation complete')

    # Open the color image in the default image viewer
    os.system('feh ' + color_image_destination)

except KeyboardInterrupt:
    # If the user interrupts the program with Ctrl+C
    print('\nProgram interrupted by the user')
except Exception as e:
    # If an error occurs
    print('An error occurred:', str(e))

finally:
    # Always close the camera, even if an error occurred
    camera.close()
