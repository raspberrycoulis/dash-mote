# dash-mote

Using the Amazon Dash Button to trigger actions on Pimoroni's [Mote kit](https://shop.pimoroni.com/products/mote-phat), in this very simple example pushing the Dash Button once will turn the Mote sticks red, and pushing the Dash Button again will turn them off.

## Requirements

In order to use this script, you will need to install a few dependencies. The simplest way is to install the Mote library from Pimoroni by running the following in your terminal:

```bash
curl https://get.pimoroni.com/motephat | bash
```

You will also need to install the `requests` Python module:

```bash
sudo pip install requests
```

Or if that fails, then you'll probably need to install the Python PIP module first:

```bash
sudo apt-get install python-pip
```
---
## Find your Amazon Dash Button's MAC address

You will need to add your Amazon Dash Button's MAC address to the `dash-mote.py` script for this to work. Details on how to find out your MAC address can be found [here](https://www.raspberrypi.org/magpi/hack-amazon-dash-button-raspberry-pi/) and then replace the following in the script:

```python
# Set your Dash Button's MAC address below
DASH_BUTTON_MAC = 'xx:xx:xx:xx:xx:xx'
```

Replace the `xx:xx:xx:xx:xx:xx` with your MAC address, but ensure **it is all lower case!**

## Running

Once installed, you can run this by simply changing into the directory and executing as follows:

```bash
cd dash-mote
sudo python dash-mote.py
```
This will then run the script - push the Amazon Dash Button and see the Mote sticks light up red; push again to turn them off.
