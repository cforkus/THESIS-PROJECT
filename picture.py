import picamera
import time
import os
import subprocess
import RPi.GPIO as GPIO

# Set the pin numbering mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the pin number for IR control
pin = 7

# Set the pin as an output pin
GPIO.setup(pin, GPIO.OUT)

# Initialize the camera
camera = picamera.PiCamera()

# Set filename for the image
filename = 'image'

# Specify the destination directory
destination = "/home/pi/ndviphotos/{}.jpg".format(filename)

try:
    # Wait for a key press to capture the image
    input('Press Enter to capture the image...')

    # Send a low signal to pin 7 to turn off IR filter
    GPIO.output(pin, GPIO.LOW)

    # Capture the image
    camera.capture(destination)

    # Print a message that the image has been captured
    print('Image captured successfully!')

    # Wait for 2 seconds before exiting
    time.sleep(2)

    # Close the camera
    camera.close()

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

finally:
    # Always close the camera and clean up GPIO settings
    camera.close()
    GPIO.cleanup()
