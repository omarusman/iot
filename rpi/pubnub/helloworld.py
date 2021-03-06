# pip3 install -U python-dotenv
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# pip3 install pubnub
from pubnub import Pubnub

pubnub = Pubnub(publish_key=os.environ.get("PUBNUB_PUB_KEY"), subscribe_key=os.environ.get("PUBNUB_SUB_KEY"))

# Go something
def callback(message, channel):
    print(message)

# Oops, oh no!
def error(message):
    print("ERROR : " + str(message))

# Hooray!
def connect(message):
    print("CONNECTED")
    print(pubnub.publish(channel=os.environ.get("PUBNUB_CHANNEL"), message='Hello from the PubNub Python SDK'))

# Reconnected, hooray!
def reconnect(message):
    print("RECONNECTED")

# Bye bye!
def disconnect(message):
    print("DISCONNECTED")


pubnub.subscribe(channels=os.environ.get("PUBNUB_CHANNEL"), callback=callback, error=callback, connect=connect, reconnect=reconnect, disconnect=disconnect)
