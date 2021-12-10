#!/usr/bin/env python3

import scapy.all as scapy
import optparse

def get_arguments():    
    parser = optparse.OptionParser()
    parser.add_option("-v", action="store_true", dest="verbose",default=False, help="Set verbose output")
    parser.add_option("-t", "--target", dest="ip_address", help="Target ip address or range (10.0.0.1/24")
    (options, arguments) = parser.parse_args()

    if not options.ip_address:
        parser.error("[-] Please specify a target IP address or range")
        exit(1)
    return options

def scan(options):
    arp_request = scapy.ARP(pdst=options.ip_address)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    if options.verbose:
        print(arp_request_broadcast.summary())
        arp_request_broadcast.show()
    targets_found = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    target_list = []
    for element in targets_found:
        target_element = { "ip": element[1].psrc, "mac": element[1].hwsrc }
        target_list.append(target_element)
        
    return(target_list)

def print_target_attributes (target_list):
    print("IP\t\tMAC")
    print("------------------------------------------------------------------------")

    for target in target_list:

        print(target["ip"] + "\t" + target["mac"])

options = get_arguments()
targets = scan(options)
print_target_attributes(targets)