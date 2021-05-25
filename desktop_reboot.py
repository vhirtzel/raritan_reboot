import re
import sys
import os
import configparser
'''
In order to use the latest Raritan SDK API bindings I've included it in this repo and the following code will add it to the path so it can be imported.
'''
api_path = os.path.abspath(os.path.join('.','pdu-python-api'))
sys.path.append(api_path)
import raritan.rpc
from raritan.rpc import pdumodel
'''
This is a basic regex pattern that will match any of the Desktop Machines in our DC because they are the only machines on these IP ranges.
This doesn't address invalid final octets but that is handled in the while loop of the main function.
'''
valid_ip = re.compile(r'65.74.(185|147).(\d*)')

'''
The main function uses a while loop to ask the user to enter the IP addresses of machines that need to be rebooted.
'''
def main():
    print("Enter IP addresses of machines needing to be rebooted.") # Print out instructions for the user
    print("Type DONE when finished.") 
    ip_lst = []
    config = parseConfig()
    user = getUser(config)
    passwd = getPass(config)                                        
    hosts = getHosts(config)
    while True:                                                     
        entry = input("")                                           # Collect a line of input from the user (this can be a copy pasted group of IPs if each IP is on a new line)
        mo = re.search(valid_ip, entry)                             # Using the regex defined above, search the user input for an IP pattern
        if entry == "DONE":                                         # This ends the loop when the user types DONE
            break
        elif (mo != None):                                          # This checks if the regex search was successful
            last_octete = mo.groups()[1]                            # Pulls out the last octet of the IP address
            last_octet_int = int(last_octete)                       # Casts the last octet into an integer so that we can compare sizes
            if (mo.groups()[0] == "185") and last_octet_int < 255:  # Checks first if the subnet is 185 then checks that the last octet is less than 255
                ip_lst.append(entry)                                # Adds the IP address string to the ip_lst list variable if it passes the check
            elif (mo.groups()[0] == "147") and last_octet_int < 30: # This checks if the subnet is 147 then checks if the last octet is less than 30 since 29 is the last IP we've added.
                ip_lst.append(entry)                                # Adds the IP address string to the ip_lst list variable if it passes the check
            else:                                                   
                print("Invalid entry, please enter an IP or type DONE")
        else:
            print("Invalid entry, please enter an IP or type DONE") 

    powercycle(user, passwd, hosts, ip_lst)

def parseConfig():
    config = configparser.ConfigParser()
    config.read('configfile.ini')
    return config

def getUser(config):
    user = config['Credentials']['user']
    return user

def getPass(config):
    passwd = config['Credentials']['passwd']
    return passwd

def getHosts(config):
    hosts = []
    for key in config['Hosts']:
        hosts.append(config['Hosts'][key])
    return hosts

def powercycle(user, passwd, hosts, ips):
    for host in hosts:
        if len(ips) == 0:
            print('All machines rebooted successfully')
            exit()
        print(f'Connecting to {host}...')
        agent = raritan.rpc.Agent("https", host, user, passwd, disable_certificate_verification = True)
        pdu = pdumodel.Pdu("model/pdu/0", agent)
        print(f'Collecting outlet data...')
        outlets = pdu.getOutlets()
        print('Getting outlet names and checking against list of IPs')
        for outlet in outlets:
            name = outlet.getSettings().name
            if name in ips:
                print(f'Rebooting {name}')
                outlet.cyclePowerState()
                ips.remove(name)


main()