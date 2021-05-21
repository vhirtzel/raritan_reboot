# desktop_reboot
Python script to reboot Desktop Minis using the Raritan API

## How to use this tool:
1) Clone this respository
2) Navigate to the root directory in the terminal and run `python3 desktop_reboot.py`
3) Follow the prompts to reboot the desired Minis.

## Requirements
* python3

## Raritan JSON-RPC API
Raritan provides an SDK that can be found [here.](https://www.raritan.com/support/product/px3)  
Documentation is included in the SDK and can also be found [here.](https://help.raritan.com/json-rpc/pdu/v3.6.1/)

There are some "raritan" pypi packages but they are for older versions of the SDK that aren't compatible with our PDUs. 

So I've bundled the Python API bindings with this repo to give a batteries included experience. 

## To Do:
* Improve the user feedback and error handling. 
* Find a way to automate the creation of the dictionary for future machine additions.