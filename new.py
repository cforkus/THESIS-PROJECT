import subprocess
import time
import os

# Set filename for the image
filename = 'image.jpg'

# Specify the destination directory
destination = "/home/pi/ndviphotos/{}".format(filename)

try:
    # Wait for a key press to capture the image
    input('Press Enter to capture the image...')

    # Capture the image using raspistill with IR-cut filter
    subprocess.run(['raspistill', '-o', destination])

    # Print a message that the image has been captured
    print('Image captured successfully!')

    # Wait for 2 seconds before exiting
    time.sleep(2)

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
    print('\nProgram interrupted by user')
except Exception as e:
    # If an error occurs
    print('An error occurred:', str(e))
