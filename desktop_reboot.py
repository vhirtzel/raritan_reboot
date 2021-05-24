import re
import sys
import os
'''
In order to use the latest Raritan SDK API bindings I've included it in this repo and the following code will add it to the path so it can be imported.
'''
api_path = os.path.abspath(os.path.join('.','pdu-python-api'))
sys.path.append(api_path)
import raritan.rpc
from raritan.rpc import pdumodel
'''
I've defined a few variables and dictionaries here at the top that model which PDUs and which Outlets in each PDU the Desktop Machines are plugged in to.
First the IP addresses of the PDUs are stored in variables as I access them a few times in the program.
'''
user = ''
passwd = ''
credentials = open('credential.conf')
for line in credentials:
    lst = []
    lst = line.split()
    if lst[0] == 'user':
        user = lst[2]
    if lst[0] == 'passwd':
        passwd = lst[2]
rack1front = '10.108.45.161'
rack1back = '10.108.45.162'
rack2front = '10.108.45.163'
rack2back = '10.108.45.164'
rack3front = '10.108.45.165'
rack3back = '10.108.45.166'
rack4front = '10.108.45.167'
rack4back = '10.108.45.168'

'''
Finally this is a basic regex pattern that will match any of the Desktop Machines in our DC because they are the only machines on these IP ranges.
This doesn't address invalid final octets but that is handled in the while loop of the main function.
'''
valid_ip = re.compile(r'65.74.(185|147).(\d*)')

'''
The main function uses a while loop to ask the user to enter the IP addresses of machines that need to be rebooted.
'''
def main():
    print("Enter IP addresses of machines needing to be rebooted.") # Print out instructions for the user
    print("Type DONE when finished.") 
    ip_lst = []                                                     # Define an empty list to store the IPs
    hosts = [
        rack1front, 
        rack1back, 
        rack2front, 
        rack2back, 
        rack3front,
        rack3back,
        rack4front,
        rack4back,
        ]
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

    powercycle(hosts, ip_lst)

def powercycle(hosts, ips):
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