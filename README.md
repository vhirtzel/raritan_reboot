# desktop_reboot
Python script to reboot Desktop Minis using the Raritan API

## How to use this tool:
0) Update your Raritan PDU labels for all of your outlets with the IPv4 addresses of the minis plugged in.
1) Clone this respository
2) In the root directory create a file called `configfile.ini` that follows the format outlined below.
3) Navigate to the root directory in the terminal and run `python3 desktop_reboot.py`
4) Follow the prompts to reboot the desired Minis.

## Requirements
* python3
* configfile.ini that has the following format:
```
[Credentials]
user = '(your Raritan PDU username here)'
passwd = '(your Raritan PDU password here)'

[Hosts]
rack1front = '(ip address for your rack1front pdu)
rack1back = '(ip address for your rack1back pdu)'
```

## Raritan JSON-RPC API
Raritan provides an SDK that can be found [here.](https://www.raritan.com/support/product/px3)  
Documentation is included in the SDK and can also be found [here.](https://help.raritan.com/json-rpc/pdu/v3.6.1/)

There are some "raritan" pypi packages but they are for older versions of the SDK that aren't compatible with our PDUs. 

So I've bundled the Python API bindings with this repo to give a batteries included experience. 

## To Do:
* Improve the user feedback and error handling. 
* Find a way to automate the creation of the dictionary for future machine additions. ✅
* Find a way to make the IP check regex to be DC agnostic
