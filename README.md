# desktop_reboot
Python script to reboot Desktop Minis using the Raritan API

## How to use this tool:
0) Update your Raritan PDU labels for all of your outlets with the IPv4 addresses of the minis plugged in.
1) Clone this respository
2) Create a virtual environment `python3 -m venv .venv`
3) Enter the environment: `source .venv/bin/activate`
4) Install the requirements `pip install -r requirements.txt` 
5) In the root directory create a file called `configfile.ini` that follows the format outlined below.
6) Navigate to the root directory in the terminal and run `python3 desktop_reboot.py`
7) Follow the prompts to reboot the desired Minis.

## Requirements
* Python >= 3.9
* configfile.ini that has the following format:
```
[Credentials]
user = '(your Raritan PDU username here)'
passwd = '(your Raritan PDU password here)'

[Hosts]
rack1front = '(ip address for your rack1front pdu)
rack1back = '(ip address for your rack1back pdu)'
```

## What is happening:
First the script gathers the IPs that need to be rebooted from the user. I've implemented strict checking using regex because we label our PDU using the IPv4 address of the minis, however all the Raritan PDU is looking for in the `powercycle` function is for the label of the outlet to match the user input.  

Next the script checks if the user didn't enter any IPs and quits if this is true. If not it connects to each individual PDU one at a time using the `Agent` class and uses the `Pdu` class and the `getOutlets()` and `getSettings().name` methods to determine the name of each outlet.  

Then it checks that name against the list of names provided by the user. If it finds a match it uses the `cyclePowerState()` method to cycle that outlet rebooting the Mini.  

Finally the script removes that IP entry from the list of requested reboots and checks to see if that was the last entry. If not it continues to the next PDU.  

## Raritan JSON-RPC API
Raritan provides an SDK that can be found [here.](https://www.raritan.com/support/product/px3)  
Documentation is included in the SDK and can also be found [here.](https://help.raritan.com/json-rpc/pdu/v3.6.1/)

There are some "raritan" pypi packages but they are for older versions of the SDK that aren't compatible with our PDUs. 

So I've bundled the Python API bindings with this repo to give a batteries included experience. 

## To Do:
* Improve the user feedback and error handling. 
* Find a way to automate the creation of the dictionary for future machine additions. ✅
* Find a way to make the IP check regex to be DC agnostic
