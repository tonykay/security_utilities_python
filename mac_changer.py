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
  print("[+] Changing MAC address for " + interface + " to " + new_mac_address)
  subprocess.call(["ifconfig", interface, "down"])
  subprocess.call(["ifconfig", interface, "hw", "ether", new_mac_address])
  subprocess.call(["ifconfig", interface, "up"])
  print("[+] ifconfig " + interface)

options = get_arguments()
# change_mac(options.interface, options.new_mac_address)

ifconfig_result_bytes = subprocess.check_output(["ifconfig", options.interface])
ifconfig_result = ifconfig_result_bytes.decode()
print(ifconfig_result)

ether_search_result = re.search(r"ether (\w\w:){5}\w\w", ifconfig_result) # .re.search(r"(\w\w:){5}\w\w")
mac_address_search_result = ether_search_result.group(0).replace("ether ","")
print(mac_address_search_result)