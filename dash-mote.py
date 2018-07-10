#!/usr/bin/env python

#####################################################################################
# This script will allow you to use an Amazon Dash Button to toggle two functions.  #
# In this case, it toggles Mote sticks by Pimoroni, but the functions can be        #
# anything you like!                                                                #
#                                                                                   #
# By Wesley Archer (AKA. @raspberrycoulis)                                          #
# https://raspberrycoulis.com | https://github.com/raspberrycoulis                  #
#                                                                                   #
# Special thanks to OyaMist Aeroponics on Raspberry Pi Stack Exchange for their     #
# assistance with this --> https://github.com/oyamist                               #
#####################################################################################

# Import the required modules
import RPi.GPIO as GPIO
import time
import requests
import logging
import urllib
import httplib
import os
import threading

try:
    import motephat
except ImportError:
    exit("This script requires the Mote pHAT library from Pimoroni!\nInstall with 'curl https://get.pimoroni.com/motephat | bash'")

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

# Set your Dash Button's MAC address below
DASH_BUTTON_MAC = 'xx:xx:xx:xx:xx:xx'

# Set he Mote brightness
motephat.set_brightness(1)

# Function to turn on the Mote sticks
def mote_on():
    motephat.set_all(255, 0, 0)
    motephat.show()


# Function to turn off the Mote sticks
def mote_off():
    motephat.set_all(0, 0, 0)
    motephat.show()

# Function that sets the lackClick variable when the Dash Button is pushed
def button_pressed_dash():
    global lastClick
    lastClick = time.time()

# This function sets and handles the states set by the button pushes
def state_machine():
    STATE1 = 1
    STATE2 = 2
    INITIAL_STATE = STATE1
    DEBOUNCE_SECONDS = 1
    state = INITIAL_STATE
    global lastClick
    lastClick = 0 # wait for next button click
    while True:
        elapsed = time.time() - lastClick
        ###### state definitions and transitions
        if state == STATE1:  # STATE1 actions and transitions
           if lastClick != 0 and elapsed > DEBOUNCE_SECONDS:
               mote_on()
               lastClick = 0  # we handled click
               state = STATE2  # goto STATE2
        elif state == STATE2:  # STATE2 actions and transitions
           if lastClick != 0 and elapsed > DEBOUNCE_SECONDS:
               mote_off()
               lastClick = 0  # we handled click
               state = INITIAL_STATE
        time.sleep(0.1)

# This is required to get the UDP packet sent by the Dash Button when pushed.
def udp_filter(pkt):
    if pkt.haslayer(DHCP):
        options = pkt[DHCP].options
        for option in options:
            if isinstance(option, tuple):
                if 'requested_addr' in option:
                    mac_to_action[pkt.src]()
                    break

# Below is required to ensure the Dash Button is detected when pushed.
mac_to_action = {DASH_BUTTON_MAC : button_pressed_dash} # Add your Amazon Dash Button's MAC address in lowercase
mac_id_list = list(mac_to_action.keys())
# create separate thread for state machine
stateMachineThread = threading.Timer(0.1, state_machine)
stateMachineThread.daemon = True
stateMachineThread.start()
sniff(prn=udp_filter, store=0, filter="udp", lfilter=lambda d: d.src in mac_id_list)
