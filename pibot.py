import RPi.GPIO as GPIO
import time
import sys
import re

pinLB = 10
pinLF = 9
pinsL = (pinLF, pinLB)

pinRB = 8
pinRF = 7
pinsR = (pinRF, pinRB)

pwmFreq = 20
pwmDutyCycle = 30
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
    setPwm((pwmDutyCycle,pwmStop,pwmDutyCycle,pwmStop))

def backwards():
    setPwm((pwmStop,pwmDutyCycle,pwmStop,pwmDutyCycle))

def right():
    setPwm((pwmDutyCycle,pwmStop,pwmStop,pwmDutyCycle))

def left():
    setPwm((pwmStop,pwmDutyCycle,pwmDutyCycle,pwmStop))

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
        time.sleep(duration)
    except KeyError:
        print "Unknown command %s" % command

def runProgram(program):
    commands = re.findall('([a-zA-Z])([0-9])', program)
    for command in commands:
        runCommand(*command)
    stop()
    GPIO.cleanup()

if __name__ == '__main__':
    runProgram(sys.argv[1])







