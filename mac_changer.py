#!/usr/bin/env python3

import subprocess

sp = subprocess

# interface = "eth0"
# new_mac_address = "00:11:22:33:44:66"

interface = input("Enter interface: ")
new_mac_address = input("Enter new new MAC in nn:nn:nn:nn:nn:nn format: ")

def mac_change():
  print("[+] Changing MAC address for " + interface + " to " + new_mac_address)
  sp.call(["ifconfig", interface, "down"])
  sp.call(["ifconfig", interface, "hw", "ether", new_mac_address])
  sp.call(["ifconfig", interface, "up"])
  print("[+] ifconfig " + interface)

def mac_output():
  print("[+] Changing MAC address for " + interface + " to " + new_mac_address)
  print("ifconfig " + interface + " down")
  print("ifconfig " + interface + " hw ether " + new_mac_address)
  print("ifconfig " + interface + " up")
  print("[+] ifconfig " + interface)

# mac_change()
mac_output()
sp.call(["ifconfig ", interface], shell=True)