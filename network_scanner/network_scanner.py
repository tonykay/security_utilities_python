#!/usr/bin/env python3

import scapy.all as scapy
import optparse
import re


def get_arguments():    
    parser = optparse.OptionParser()
    parser.add_option("-v", action="store_true", dest="verbose",default=False, help="Set verbose output")
    # parser.add_option("-v", "--verbose", dest="verbose", help="Verbose output")
    (options, arguments) = parser.parse_args()
    # if not options.verbose:
    #     verbose = False
    return options

def scan(ip_address, options):
    arp_request = scapy.ARP(pdst=ip_address)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    if options.verbose:
        print(arp_request_broadcast.summary())
        arp_request_broadcast.show()

    # print(arp_request.summary())
    # print(broadcast.summary())
    # scapy.ls(scapy.ARP())
    # scapy.ls(scapy.Ether())

#verbose = False
options = get_arguments()

scan("10.211.55.1/24", options)