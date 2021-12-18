#!/usr/bin/env python3

import requests
import json
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-d", "--domain", type=str, help="Domain of FQDN output verbosity")
    parser.add_argument("-j", "--json", help="Output in JSON", action="store_true")
    args = parser.parse_args()
    # if args.verbose:
    #     print("verbosity turned on")
    # if not args.domain:
    #     parser.error("[-] Please specify a domain, use --help for more info.")
    return args

if __name__ == "__main__":
    args = get_arguments()
    r = requests.get("https://" + args.domain)
    if args.json:
        print(json.dumps(dict(r.headers), indent=2))
    else:
         print(r.headers)
