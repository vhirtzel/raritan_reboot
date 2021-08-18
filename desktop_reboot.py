import configparser

from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt


import raritan.rpc
from raritan.rpc import pdumodel

console = Console()
layout = Layout()

# Divide the "screen" in to three parts
layout.split(
    Layout(name="header", size=3),
    Layout(ratio=1, name="main"),
    Layout(size=10, name="user_prompts"),
)
# Divide the "main" layout in to "side" and "body"
layout["main"].split_row(
    Layout(name="ip_list"),
    Layout(name="status", ratio=2),
)
layout["header"].update(
    Layout(
        Panel(
            "Desktop Machine Reboot",
        )
    )
)

ip_table = Table(expand=True)
ip_table.add_column("IPs")
layout["ip_list"].update(Layout(ip_table))

status_table = Table(expand=True)
status_table.add_column("Status")
layout["status"].update(Layout(status_table))

def main():
    console.print(layout)
    ip_lst = []
    config = parseConfig()
    user = getUser(config)
    passwd = getPass(config)
    hosts = getHosts(config)
    layout["user_prompts"].update(
        Layout(
            Panel(
                "Enter IP addresses of machines needing to be rebooted"
            )
        )
    )
    console.print(layout)
    while True:
        entry = Prompt.ask("Type DONE when finished")
        if entry == "DONE":
            break
        check_entry = check_valid_ip(config, entry)
        if check_entry == True:
            ip_lst.append(entry)
            ip_table.add_row(entry)

    with Live(layout, refresh_per_second=4):
        powercycle(user, passwd, hosts, ip_lst)


def parseConfig():
    config = configparser.ConfigParser()
    config.read("configfile.ini")
    status_table.add_row("Reading Config... ✅")
    return config


def getUser(config):
    user = config["Credentials"]["user"]
    status_table.add_row("Getting Raritan PDU Username... ✅")
    return user


def getPass(config):
    passwd = config["Credentials"]["passwd"]
    status_table.add_row("Getting Raritan PDU Password... ✅")
    return passwd


def getHosts(config):
    hosts = []
    for key in config["Hosts"]:
        hosts.append(config["Hosts"][key])
    status_table.add_row("Getting Raritan PDU IPs... ✅")
    return hosts

def check_valid_ip(config, entry):
    entry_lst = entry.split(".")
    for ip_range in config["IP Ranges"]:
        range_str = config["IP Ranges"][ip_range]
        lst = range_str.split(".")
        if entry_lst[:3] != lst[:3]:
            continue
        range_lst = lst[3].split(":")
        if int(entry_lst[3]) in range(int(range_lst[0]),int(range_lst[1])+1):
            return True
    
    print(f"IP Address not found in range {range_str}")
    print("Please enter a valid IP or type DONE")
    return False

        


def powercycle(user, passwd, hosts, ips):
    for host in hosts:
        if len(ips) == 0:
            layout["user_prompts"].update(
                Layout(Panel("All machines rebooted successfully!"))
            )
            exit()
        status_table.add_row(f"Connecting to {host}...")
        agent = raritan.rpc.Agent(
            "https", host, user, passwd, disable_certificate_verification=True
        )
        pdu = pdumodel.Pdu("model/pdu/0", agent)
        status_table.add_row("Collecting outlet data...")
        outlets = pdu.getOutlets()
        status_table.add_row("Checking outlet data against list of IPs")
        for outlet in outlets:
            name = outlet.getSettings().name
            if name in ips:
                status_table.add_row(f"Rebooting {name}")
                outlet.cyclePowerState()
                ips.remove(name)
                if len(ips) == 0:
                    status_table.add_row("All machines rebooted successfully")
                    exit()


if __name__ == "__main__":
    main()
