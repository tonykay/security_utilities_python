#!/usr/bin/env python3

import requests
import json
import argparse
import socket

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-t", "--target", type=str, help="Target: Hostname, FQDN, or Domain")
    parser.add_argument("-j", "--json", help="Output in JSON", action="store_true")
    args = parser.parse_args()
    # if args.verbose:
    #     print("verbosity turned on")
    # if not args.domain:
    #     parser.error("[-] Please specify a domain, use --help for more info.")
    return args


if __name__ == "__main__":
    args = get_arguments()
    target_ip = socket.gethostbyname(args.target)
    target_dict = {
        'ip_addr': target_ip 
    }

    r = requests.get("https://" + args.target)
    if args.json:
        print(json.dumps(dict(r.headers), indent=2))
        print(json.dumps(target_dict,indent=2))
        # print(f'{ \"target_ip\": "{target_ip}"}','\n')
    else:
        print(r.headers,"\n")
        print(f"IP address of {args.target} is {target_ip}","\n")

