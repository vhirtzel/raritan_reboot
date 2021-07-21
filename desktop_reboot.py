import re
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

# Regex to capture valid machine IPs
valid_ip = re.compile(r"65.74.(185|147).(\d*)")


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
        mo = re.search(valid_ip, entry)
        if entry == "DONE":
            break
        elif mo is not None:
            last_octete = mo.groups()[1]
            last_octet_int = int(last_octete)
            if (mo.groups()[0] == "185") and last_octet_int < 255:
                ip_lst.append(entry)
                ip_table.add_row(entry)
            elif (mo.groups()[0] == "147") and last_octet_int < 40:
                ip_lst.append(entry)
                ip_table.add_row(entry)
            else:
                print("Invalid entry, please enter an IP or type DONE")
        else:
            print("Invalid entry, please enter an IP or type DONE")
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
