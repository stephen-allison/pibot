import pibot
import sys


if __name__ == "__main__":
    pwmL = float(sys.argv[1])
    pwmR = float(sys.argv[2])
    pibot.pwmDutyCycleR = pwmR
    pibot.pwmDutyCycleL = pwmL

    pibot.runProgram("f30")
