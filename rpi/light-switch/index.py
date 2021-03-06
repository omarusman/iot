# pip3 install -U python-dotenv
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# pip3 install pubnub
from pubnub import Pubnub

pubnub = Pubnub(publish_key=os.environ.get("PUBNUB_PUB_KEY"), subscribe_key=os.environ.get("PUBNUB_SUB_KEY"))

# GPIO
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

CONTROL_PIN = 11
HERTZ = 50

OFF = 70
ON = 120
WAIT = 90

GPIO.setup(CONTROL_PIN, GPIO.OUT)
PWM = GPIO.PWM(CONTROL_PIN, HERTZ)
PWM.start(7)

# Rotate the servo in a specific degrees.
def rotateServo(degree):
    DC = 1./18. * (degree) + 2
    PWM.ChangeDutyCycle(DC)
    time.sleep(0.05)

# Make sure message can be rerpresented in a float.
def rotate(message):
    try:
        value = str(message)

        if value == "off":
            rotateServo(OFF)

        if value == "on" :
            rotateServo(ON)

        time.sleep(1)
        rotateServo(WAIT)

    except ValueError:
        pass
    except TypeError:
        pass

# Go something
def callback(message, channel):
    print(message)

    rotate(message)


# Oops, oh no!
def error(message):
    print("ERROR : " + str(message))

# Hooray!
def connect(message):
    print("CONNECTED")
    print(pubnub.publish(channel=os.environ.get("PUBNUB_CHANNEL"), message='Hello from the Servo'))

# Reconnected, hooray!
def reconnect(message):
    print("RECONNECTED")

# Bye bye!
def disconnect(message):
    print("DISCONNECTED")


pubnub.subscribe(channels=os.environ.get("PUBNUB_CHANNEL"), callback=callback, error=callback, connect=connect, reconnect=reconnect, disconnect=disconnect)
