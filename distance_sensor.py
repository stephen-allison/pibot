# CamJam EduKit 3 - Robotics
# Worksheet 6 – Measuring Distance
import RPi.GPIO as GPIO # Import the GPIO Library
import time # Import the Time library
# Set the GPIO modes


def measureDistance():
    # Set trigger to False (Low)
    GPIO.output(pinTrigger, False)
    # Allow module to settle
    time.sleep(0.5)
    # Send 10us pulse to trigger
    GPIO.output(pinTrigger, True)
    time.sleep(0.00001)
    GPIO.output(pinTrigger, False)
    # Start the timer
    startTime = time.time()
    # The start time is reset until the Echo pin is taken high (==1)
    while GPIO.input(pinEcho)==0:
        startTime = time.time()
    # Stop when the Echo pin is no longer high - the end time
    while GPIO.input(pinEcho)==1:
        stopTime = time.time()
        # If the sensor is too close to an object, the Pi cannot # see the echo quickly enough, so it has to detect that # problem and say what has happened
        if stopTime-startTime >= 0.04:
                print("Hold on there!  You're too close for me to see.")
                stopTime = startTime
                break
    # Calculate pulse length
    elapsedTime = stopTime - startTime
    # Distance pulse travelled in that time is
    # time multiplied by the speed of sound (cm/s)
    distance = elapsedTime * 34326
    # That was the distance there and back so halve the value
    distance = distance / 2
    return distance


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Define GPIO pins to use on the Pi
pinTrigger = 17
pinEcho = 18
GPIO.setup(pinTrigger, GPIO.OUT)  # Trigger
GPIO.setup(pinEcho, GPIO.IN)      # Echo

try:
    # Repeat the next indented block forever
    while True:
        d = measureDistance()
        print("Distance : %.1f" % distance)
        time.sleep(0.5)

# If you press CTRL+C, cleanup and stop
except KeyboardInterrupt:
# Reset GPIO settings
    GPIO.cleanup()
