#!/usr/bin/env python3

import subprocess
import optparse
import re

def get_arguments():    
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac_address", help="New MAC address (format nn:nn:nn:nn:nn:nn)")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac_address:
        parser.error("[-] Please specify a new MAC, use --help for more info.")
    return options

def change_mac(interface, new_mac_address):
    print("[+] Changing MAC address for " + interface + ": " + new_mac_address)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac_address])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac_address(interface):
    ifconfig_result = (subprocess.check_output(["ifconfig", interface])).decode()
    ether_line_result = re.search(r"ether (\w\w:){5}\w\w", ifconfig_result) 
    if ether_line_result:
        mac_address_search_result = ether_line_result.group(0).replace("ether ","")
        return(mac_address_search_result)
    else:
        print("[-] Could not read MAC address.")
        exit(1)


if __name__ == "__main__":
    options = get_arguments()
    starting_mac = (get_current_mac_address(options.interface))
    change_mac(options.interface, options.new_mac_address)
    ending_mac = (get_current_mac_address(options.interface))

    if ending_mac == options.new_mac_address:
        print("[+] Success")
    else:
        print("[-] Failed")

    print("[+] Starting MAC for         " + options.interface + ": " + starting_mac)
    print("[+] Ending MAC for           " + options.interface + ": " + ending_mac)