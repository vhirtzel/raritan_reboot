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

'''Then I created a dictionary where the keys are the IPs of the machines 
and the values are a list containing which PDU they are plugged in to and the number of the outlet it is plugged in to.
'''
desktopPDU = {
    '65.74.185.2': [rack1front, '47'],
    '65.74.185.3': [rack1front, '46'],
    '65.74.185.4': [rack1front, '45'],
    '65.74.185.5': [rack1front, '44'],
    '65.74.185.6': [rack1front, '43'],
    '65.74.185.7': [rack1front, '42'],
    '65.74.185.8': [rack1front, '41'],
    '65.74.185.9': [rack1front, '40'],
    '65.74.185.10': [rack1front, '39'],
    '65.74.185.11': [rack1front, '38'],
    '65.74.185.12': [rack1front, '37'],
    '65.74.185.13': [rack1front, '36'],
    '65.74.185.14': [rack1front, '35'],
    '65.74.185.15': [rack1front, '34'],
    '65.74.185.16': [rack1front, '33'],
    '65.74.185.17': [rack1front, '32'],
    '65.74.185.18': [rack1front, '31'],
    '65.74.185.19': [rack1front, '30'],
    '65.74.185.20': [rack1front, '29'],
    '65.74.185.21': [rack1front, '28'],
    '65.74.185.22': [rack1front, '27'],
    '65.74.185.23': [rack1front, '26'],
    '65.74.185.24': [rack1front, '25'],
    '65.74.185.25': [rack1front, '24'],
    '65.74.185.26': [rack1front, '23'],
    '65.74.185.27': [rack1front, '22'],
    '65.74.185.28': [rack1front, '21'],
    '65.74.185.29': [rack1front, '20'],
    '65.74.185.30': [rack1front, '19'],
    '65.74.185.31': [rack1front, '18'],
    '65.74.185.32': [rack1front, '17'],
    '65.74.185.33': [rack1front, '16'],
    '65.74.185.34': [rack1front, '15'],
    '65.74.185.35': [rack1front, '14'],
    '65.74.185.36': [rack1front, '13'],
    '65.74.185.37': [rack1front, '12'],
    '65.74.185.38': [rack1front, '11'],
    '65.74.185.39': [rack1front, '10'],
    '65.74.185.40': [rack1front, '9'],
    '65.74.185.41': [rack1front, '8'],
    '65.74.185.42': [rack1back, '47'],
    '65.74.185.43': [rack1back, '46'],
    '65.74.185.44': [rack1back, '45'],
    '65.74.185.45': [rack1back, '44'],
    '65.74.185.46': [rack1back, '43'],
    '65.74.185.47': [rack1back, '42'],
    '65.74.185.48': [rack1back, '41'],
    '65.74.185.49': [rack1back, '40'],
    '65.74.185.50': [rack1back, '39'],
    '65.74.185.51': [rack1back, '38'],
    '65.74.185.52': [rack1back, '37'],
    '65.74.185.53': [rack1back, '36'],
    '65.74.185.54': [rack1back, '35'],
    '65.74.185.55': [rack1back, '34'],
    '65.74.185.56': [rack1back, '33'],
    '65.74.185.57': [rack1back, '32'],
    '65.74.185.58': [rack1back, '31'],
    '65.74.185.59': [rack1back, '30'],
    '65.74.185.60': [rack1back, '29'],
    '65.74.185.61': [rack1back, '28'],
    '65.74.185.62': [rack1back, '27'],
    '65.74.185.63': [rack1back, '26'],
    '65.74.185.64': [rack1back, '25'],
    '65.74.185.65': [rack1back, '24'],
    '65.74.185.66': [rack1back, '23'],
    '65.74.185.67': [rack1back, '22'],
    '65.74.185.68': [rack1back, '21'],
    '65.74.185.69': [rack1back, '20'],
    '65.74.185.70': [rack1back, '19'],
    '65.74.185.71': [rack1back, '18'],
    '65.74.185.72': [rack1back, '17'],
    '65.74.185.73': [rack1back, '16'],
    '65.74.185.74': [rack2front, '47'],
    '65.74.185.75': [rack2front, '46'],
    '65.74.185.76': [rack2front, '45'],
    '65.74.185.77': [rack2front, '44'],
    '65.74.185.78': [rack2front, '43'],
    '65.74.185.79': [rack2front, '42'],
    '65.74.185.80': [rack2front, '41'],
    '65.74.185.81': [rack2front, '40'],
    '65.74.185.82': [rack2front, '39'],
    '65.74.185.83': [rack2front, '38'],
    '65.74.185.84': [rack2front, '37'],
    '65.74.185.85': [rack2front, '36'],
    '65.74.185.86': [rack2front, '35'],
    '65.74.185.87': [rack2front, '34'],
    '65.74.185.88': [rack2front, '33'],
    '65.74.185.89': [rack2front, '32'],
    '65.74.185.90': [rack2front, '31'],
    '65.74.185.91': [rack2front, '30'],
    '65.74.185.92': [rack2front, '29'],
    '65.74.185.93': [rack2front, '28'],
    '65.74.185.94': [rack2front, '27'],
    '65.74.185.95': [rack2front, '26'],
    '65.74.185.96': [rack2front, '25'],
    '65.74.185.97': [rack2front, '24'],
    '65.74.185.98': [rack2front, '23'],
    '65.74.185.99': [rack2front, '22'],
    '65.74.185.100': [rack2front, '21'],
    '65.74.185.101': [rack2front, '20'],
    '65.74.185.102': [rack2front, '19'],
    '65.74.185.103': [rack2front, '18'],
    '65.74.185.104': [rack2front, '17'],
    '65.74.185.105': [rack2front, '16'],
    '65.74.185.106': [rack2front, '15'],
    '65.74.185.107': [rack2front, '14'],
    '65.74.185.108': [rack2front, '13'],
    '65.74.185.109': [rack2front, '12'],
    '65.74.185.110': [rack2front, '11'],
    '65.74.185.111': [rack2front, '10'],
    '65.74.185.112': [rack2front, '9'],
    '65.74.185.113': [rack2front, '8'],
    '65.74.185.114': [rack2back, '47'],
    '65.74.185.115': [rack2back, '46'],
    '65.74.185.116': [rack2back, '45'],
    '65.74.185.117': [rack2back, '44'],
    '65.74.185.118': [rack2back, '43'],
    '65.74.185.119': [rack2back, '42'],
    '65.74.185.120': [rack2back, '41'],
    '65.74.185.121': [rack2back, '40'],
    '65.74.185.122': [rack2back, '39'],
    '65.74.185.123': [rack2back, '38'],
    '65.74.185.124': [rack2back, '37'],
    '65.74.185.125': [rack2back, '36'],
    '65.74.185.126': [rack2back, '35'],
    '65.74.185.127': [rack2back, '34'],
    '65.74.185.128': [rack2back, '33'],
    '65.74.185.129': [rack2back, '32'],
    '65.74.185.130': [rack2back, '31'],
    '65.74.185.131': [rack2back, '30'],
    '65.74.185.132': [rack2back, '29'],
    '65.74.185.133': [rack2back, '28'],
    '65.74.185.134': [rack2back, '27'],
    '65.74.185.135': [rack2back, '26'],
    '65.74.185.136': [rack2back, '25'],
    '65.74.185.137': [rack2back, '24'],
    '65.74.185.138': [rack2back, '23'],
    '65.74.185.139': [rack2back, '22'],
    '65.74.185.140': [rack2back, '21'],
    '65.74.185.141': [rack2back, '20'],
    '65.74.185.142': [rack2back, '19'],
    '65.74.185.143': [rack2back, '18'],
    '65.74.185.144': [rack2back, '17'],
    '65.74.185.145': [rack2back, '16'],
    '65.74.185.146': [rack3front, '47'],
    '65.74.185.147': [rack3front, '46'],
    '65.74.185.148': [rack3front, '45'],
    '65.74.185.149': [rack3front, '44'],
    '65.74.185.150': [rack3front, '43'],
    '65.74.185.151': [rack3front, '42'],
    '65.74.185.152': [rack3front, '41'],
    '65.74.185.153': [rack3front, '40'],
    '65.74.185.154': [rack3front, '39'],
    '65.74.185.155': [rack3front, '38'],
    '65.74.185.156': [rack3front, '37'],
    '65.74.185.157': [rack3front, '36'],
    '65.74.185.158': [rack3front, '35'],
    '65.74.185.159': [rack3front, '34'],
    '65.74.185.160': [rack3front, '33'],
    '65.74.185.161': [rack3front, '32'],
    '65.74.185.162': [rack3front, '31'],
    '65.74.185.163': [rack3front, '30'],
    '65.74.185.164': [rack3front, '29'],
    '65.74.185.165': [rack3front, '28'],
    '65.74.185.166': [rack3front, '27'],
    '65.74.185.167': [rack3front, '26'],
    '65.74.185.168': [rack3front, '25'],
    '65.74.185.169': [rack3front, '24'],
    '65.74.185.170': [rack3front, '23'],
    '65.74.185.171': [rack3front, '22'],
    '65.74.185.172': [rack3front, '21'],
    '65.74.185.173': [rack3front, '20'],
    '65.74.185.174': [rack3front, '19'],
    '65.74.185.175': [rack3front, '18'],
    '65.74.185.176': [rack3front, '17'],
    '65.74.185.177': [rack3front, '16'],
    '65.74.185.178': [rack3front, '15'],
    '65.74.185.179': [rack3front, '14'],
    '65.74.185.180': [rack3front, '13'],
    '65.74.185.181': [rack3front, '12'],
    '65.74.185.182': [rack3front, '11'],
    '65.74.185.183': [rack3front, '10'],
    '65.74.185.184': [rack3front, '9'],
    '65.74.185.185': [rack3front, '8'],
    '65.74.185.186': [rack3back, '47'],
    '65.74.185.187': [rack3back, '46'],
    '65.74.185.188': [rack3back, '45'],
    '65.74.185.189': [rack3back, '44'],
    '65.74.185.190': [rack3back, '43'],
    '65.74.185.191': [rack3back, '42'],
    '65.74.185.192': [rack3back, '41'],
    '65.74.185.193': [rack3back, '40'],
    '65.74.185.194': [rack3back, '39'],
    '65.74.185.195': [rack3back, '38'],
    '65.74.185.196': [rack3back, '37'],
    '65.74.185.197': [rack3back, '36'],
    '65.74.185.198': [rack3back, '35'],
    '65.74.185.199': [rack3back, '34'],
    '65.74.185.200': [rack3back, '33'],
    '65.74.185.201': [rack3back, '32'],
    '65.74.185.202': [rack3back, '31'],
    '65.74.185.203': [rack3back, '30'],
    '65.74.185.204': [rack3back, '29'],
    '65.74.185.205': [rack3back, '28'],
    '65.74.185.206': [rack3back, '27'],
    '65.74.185.207': [rack3back, '26'],
    '65.74.185.208': [rack3back, '25'],
    '65.74.185.209': [rack3back, '24'],
    '65.74.185.210': [rack3back, '23'],
    '65.74.185.211': [rack3back, '22'],
    '65.74.185.212': [rack3back, '21'],
    '65.74.185.213': [rack3back, '20'],
    '65.74.185.214': [rack3back, '19'],
    '65.74.185.215': [rack3back, '18'],
    '65.74.185.216': [rack3back, '17'],
    '65.74.185.217': [rack3back, '16'],
    '65.74.185.218': [rack4front, '47'],
    '65.74.185.219': [rack4front, '46'],
    '65.74.185.220': [rack4front, '45'],
    '65.74.185.221': [rack4front, '44'],
    '65.74.185.222': [rack4front, '43'],
    '65.74.185.223': [rack4front, '42'],
    '65.74.185.224': [rack4front, '41'],
    '65.74.185.225': [rack4front, '40'],
    '65.74.185.226': [rack4front, '39'],
    '65.74.185.227': [rack4front, '38'],
    '65.74.185.228': [rack4front, '37'],
    '65.74.185.229': [rack4front, '36'],
    '65.74.185.230': [rack4front, '35'],
    '65.74.185.231': [rack4front, '34'],
    '65.74.185.232': [rack4front, '33'],
    '65.74.185.233': [rack4front, '32'],
    '65.74.185.234': [rack4front, '31'],
    '65.74.185.235': [rack4front, '30'],
    '65.74.185.236': [rack4front, '29'],
    '65.74.185.237': [rack4front, '28'],
    '65.74.185.238': [rack4front, '27'],
    '65.74.185.239': [rack4front, '26'],
    '65.74.185.240': [rack4front, '25'],
    '65.74.185.241': [rack4front, '24'],
    '65.74.185.242': [rack4front, '23'],
    '65.74.185.243': [rack4front, '22'],
    '65.74.185.244': [rack4front, '21'],
    '65.74.185.245': [rack4front, '20'],
    '65.74.185.246': [rack4front, '19'],
    '65.74.185.247': [rack4front, '18'],
    '65.74.185.248': [rack4front, '17'],
    '65.74.185.249': [rack4front, '16'],
    '65.74.185.250': [rack4front, '15'],
    '65.74.185.251': [rack4front, '14'],
    '65.74.185.252': [rack4front, '13'],
    '65.74.185.253': [rack4front, '12'],
    '65.74.185.254': [rack4front, '11'],
    '65.74.147.2': [rack4front, '10'],
    '65.74.147.3': [rack4front, '9'],
    '65.74.147.4': [rack4front, '8'],
    '65.74.147.5': [rack4back, '47'],
    '65.74.147.6': [rack4back, '46'],
    '65.74.147.7': [rack4back, '45'],
    '65.74.147.8': [rack4back, '44'],
    '65.74.147.9': [rack4back, '43'],
    '65.74.147.10': [rack4back, '42'],
    '65.74.147.11': [rack4back, '41'],
    '65.74.147.12': [rack4back, '40'],
    '65.74.147.13': [rack4back, '39'],
    '65.74.147.14': [rack4back, '38'],
    '65.74.147.15': [rack4back, '37'],
    '65.74.147.16': [rack4back, '36'],
    '65.74.147.17': [rack4back, '35'],
    '65.74.147.18': [rack4back, '34'],
    '65.74.147.19': [rack4back, '33'],
    '65.74.147.20': [rack4back, '32'],
    '65.74.147.21': [rack4back, '31'],
    '65.74.147.22': [rack4back, '30'],
    '65.74.147.23': [rack4back, '29'],
    '65.74.147.24': [rack4back, '28'],
    '65.74.147.25': [rack4back, '27'],
    '65.74.147.26': [rack4back, '26'],
    '65.74.147.27': [rack4back, '25'],
    '65.74.147.28': [rack4back, '24'],
    '65.74.147.29': [rack4back, '23'],
}

'''
Finally this is a basic regex pattern that will match any of the Desktop Machines in our DC because they are the only machines on these IP ranges.
This doesn't address invalid final octets but that is handled in the while loop of the main function.
'''
valid_ip = re.compile(r'65.74.(185|147).(\d*)')

'''
The main function uses a while loop to ask the user to enter the IP addresses of machines that need to be rebooted.
I thought about using the pyperclip module to just read the system clipboard and automatically pull out the valid IPs.
However this would require the users installing the pyperclips module using pip which can get complicated. 
I need to do research on how to easily distribute python scripts with non standard library modules as dependencies before trying something like that.
'''
def main():
    print("Enter IP addresses of machines needing to be rebooted.") # Print out instructions for the user
    print("Type DONE when finished.") 
    ip_lst = []                                                     # Define an empty list to store the IPs
    outlets = {
        rack1front: [], 
        rack1back: [], 
        rack2front: [], 
        rack2back: [], 
        rack3front: [],
        rack3back: [],
        rack4front: [],
        rack4back: [],
        }
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

    for ip in ip_lst:                                               
        if desktopPDU[ip][0] == rack1front:                            # These if statements checks the first list entry for the key values 'desktopPDU' dictionary.
            outlets[rack1front].append(desktopPDU[ip][1])               # If the IP address key matches the if statement it will update the corresponding list defined above.
        if desktopPDU[ip][0] == rack1back:                             # It will use the second list entry for the 'desktopPDU' dictionary key values to update the outlet list with the outlet of that IP.
            outlets[rack1back].append(desktopPDU[ip][1])
        if desktopPDU[ip][0] == rack2front:
            outlets[rack2front].append(desktopPDU[ip][1])
        if desktopPDU[ip][0] == rack2back:
            outlets[rack2back].append(desktopPDU[ip][1])
        if desktopPDU[ip][0] == rack3front:
            outlets[rack3front].append(desktopPDU[ip][1])
        if desktopPDU[ip][0] == rack3back:
            outlets[rack3back].append(desktopPDU[ip][1])
        if desktopPDU[ip][0] == rack4front:
            outlets[rack4front].append(desktopPDU[ip][1])
        if desktopPDU[ip][0] == rack4back:
            outlets[rack4back].append(desktopPDU[ip][1])

    for host in outlets:
        if len(outlets[host]) > 0:
            powercycle(host, outlets[host])

def powercycle(host, list):
    agent = raritan.rpc.Agent("https", host, user, passwd, disable_certificate_verification = True)
    pdu = pdumodel.Pdu("model/pdu/0", agent)
    outlets = pdu.getOutlets()
    for outlet in list:
        outlets[int(outlet)+1].cyclePowerState()

main()