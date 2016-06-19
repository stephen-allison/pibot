import RPi.GPIO as GPIO
import time
import sys
import re
from datetime import datetime, timedelta
import distance_sensor

pinLB = 10
pinLF = 9
pinsL = (pinLF, pinLB)

pinRB = 8
pinRF = 7
pinsR = (pinRF, pinRB)

pwmFreq = 20
pwmDutyCycleR = 30
pwmDutyCycleL = 28
pwmStop = 0


def initGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for pin in pinsL + pinsR:
        GPIO.setup(pin, GPIO.OUT)

    pwmPins = [GPIO.PWM(pin, pwmFreq) for pin in pinsL + pinsR]

    for pwmPin in pwmPins:
        pwmPin.start(pwmStop)

    return pwmPins

pwmPins = initGPIO()

def stop():
    for pin in pwmPins:
        pin.ChangeDutyCycle(pwmStop)

def setPwm(dutyCycles):
    for (dc, pin) in zip(dutyCycles, pwmPins):
        pin.ChangeDutyCycle(dc)

def forwards():
    setPwm((pwmDutyCycleL,pwmStop,pwmDutyCycleR,pwmStop))

def backwards():
    setPwm((pwmStop,pwmDutyCycleL,pwmStop,pwmDutyCycleR))

def right():
    setPwm((pwmDutyCycleL,pwmStop,pwmStop,pwmDutyCycleR))

def left():
    setPwm((pwmStop,pwmDutyCycleL,pwmDutyCycleR,pwmStop))

COMMANDS = {
    'f': forwards,
    'b': backwards,
    'r': right,
    'l': left,
    's': stop
}

def runCommand(command, duration):
    try:
        action = COMMANDS[command]
        action()
        time.sleep(float(duration)/10.0)
    except KeyError:
        print "Unknown command %s" % command

def runProgram(program):
    commands = re.findall('([a-zA-Z])([0-9]*)', program)
    for command in commands:
        runCommand(*command)
    stop()
    GPIO.cleanup()

def avoider():
    start = datetime.now()
    runfor = timedelta(minutes=2)

    while datetime.now() - start < runfor:
        runProgram('f1')
        d = distance_sensor.measureDistance()
        if d < 8:
            runProgram('b5r10')


if __name__ == '__main__':
    if sys.argv[1] == 'avoider':
        avoider()
    else:
        runProgram(sys.argv[1])







