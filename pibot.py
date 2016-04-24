import RPi.GPIO as GPIO


pinLF = 10
pinLB = 9
pinsL = (pinLF, pinLB)

pinRF = 8
pinRB = 7
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

forwards()
time.sleep(1)
right()
time.sleep(0.5)
backwards()
time.sleep(1)
stop()
GPIO.cleanup()

