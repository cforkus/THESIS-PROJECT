import time
import os
import subprocess

# Set the filename for the image
filename = 'image'

# Specify the destination directory
destination = "/home/pi/ndviphotos/{}.jpg".format(filename)

# Disable camera effects and image processing
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0
camera.awb_mode = 'off'
camera.exposure_mode = 'auto'

try:
    # Wait for a key press to capture the image
    input('Press Enter to capture the image...')

    # Capture the image using raspistill
    subprocess.run(['raspistill', '-o', destination])

    # Print a message that the image has been captured
    print('Image captured successfully!')

    # Check if feh is installed, and install it if not
    feh_check = subprocess.run(['which', 'feh'], capture_output=True, text=True)
    if feh_check.returncode != 0:
        print('feh is not installed, installing...')
        subprocess.run(['sudo', 'apt-get', 'update'])
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'feh'])
        print('feh installation complete')

    # Open in the default image viewer
    os.system('feh ' + destination)

except KeyboardInterrupt:
    # If the user interrupts the program with Ctrl+C
    print('\nProgram interrupted by the user')
except Exception as e:
    # If an error occurs
    print('An error occurred:', str(e))
