import configparser
import threading

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
        Layout(Panel("Enter IP addresses of machines needing to be rebooted. Type DONE when finished"))
    )
    console.print(layout)
    while True:
        entry = Prompt.ask()
        if entry == "DONE":
            break
        #check_entry = check_valid_ip(config, entry)
        check_entry = True
        if check_entry is True:
            ip_lst.append(entry)
            ip_table.add_row(entry)
    layout["user_prompts"].update(Layout(Panel(str(ip_lst))))
    with Live(layout, refresh_per_second=4):
        jobs = []
        for host in hosts:
            jobs.append(threading.Thread(target=powercycle, args=(user, passwd, host, ip_lst), daemon=True))

        [j.start() for j in jobs]
        [j.join() for j in jobs]


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
        if int(entry_lst[3]) in range(int(range_lst[0]), int(range_lst[1]) + 1):
            return True

    print(f"IP Address not found in range {range_str}")
    print("Please enter a valid IP or type DONE")
    return False


reboot_lock = threading.RLock()


def powercycle(user, passwd, host, ips):
    status_table.add_row(f"Connecting to {host}...")
    agent = raritan.rpc.Agent(
        "https", host, user, passwd, disable_certificate_verification=True
    )
    pdu = pdumodel.Pdu("model/pdu/0", agent)
    status_table.add_row(f"Collecting outlet data for {host}...")
    outlets = pdu.getOutlets()
    status_table.add_row(f"Checking outlet data for {host} against list of IPs")
    for outlet in outlets:
        name = outlet.getSettings().name
        if name in ips:
            with reboot_lock:
                status_table.add_row(f"Rebooting {name}")
                outlet.cyclePowerState()
                ips.remove(name)
                layout["user_prompts"].update(Layout(Panel(str(ips))))
        if len(ips) == 0:
            layout["user_prompts"].update(Layout(Panel("Done")))
            exit()


if __name__ == "__main__":
    main()
