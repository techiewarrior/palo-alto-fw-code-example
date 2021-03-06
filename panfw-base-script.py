# Written by -
# Description -
# Date -

import string
import getpass
import subprocess
import argparse
import urllib3
import ssl
import re
import os
import sys
import logging
import requests
import xml.etree.ElementTree as ET
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

# Handler for the command line arguments, if used.
parser = argparse.ArgumentParser()
# parser.add_argument("-f", "--firewall", help="Device name or IP", default="")  # Example using default arg.
parser.add_argument("-f", "--firewall", help="Device name or IP")
parser.add_argument("-u", "--username", help="Username")
parser.add_argument("-p", "--password", help="Password")
parser.add_argument("-k", "--apikey", help="API Key")
parser.add_argument("-l", "--log", default="WARNING")

args = parser.parse_args()

try:
    lnum = getattr(logging, args.log.upper())
except:
    lnum = 20

logging.basicConfig(format='%(message)s', level=lnum)
args = parser.parse_args()

if args.firewall:
    firewall = args.firewall
else:
    firewall = input("Enter Panorama IP: ")


def determinehost(passhost):
    # Enter shortnames for firewalls.
    iptoc = {'TEST': '192.168.1.1'}

    if passhost not in iptoc:
        print("Preset firewall value list exist for: "),
        for item in iptoc:
            print(item,)
        print
        return passhost
    else:
        host = iptoc[passhost]
        return host


def printdes(s, o=''):
    print ("\n  " + sys.argv[0] + " - " + s)
    olist = o.split(",")
    if 'printul' in olist:
        tl = len(sys.argv[0]) + len(s) + 7
        print("-"*tl)
    else:
        print("")


def send_api_request(url, values):
    response = requests.get(url, params=values, verify=False)
    return response.text


def get_api_key(hostname, username, password):
    try:
        url = 'https://' + hostname + '/api'
        values = {'type': 'keygen', 'user': username, 'password': password}
        response = requests.get(url, params=values, verify=False)
        return ET.fromstring(response.text).find('.//result/key').text
    except:
        raise ValueError("Unable to generate API key from firewall.")


def fetch_api_key():
    try:
        if args.apikey:
            apikey = args.apikey
        else:
            if args.username:
                username = args.username
            else:
                username = input("Enter the user login:  ")
            if args.password:
                password = args.password
            else:
                password = getpass.getpass(prompt="Enter the password:  ")

            return get_api_key(iptoc[args.firewall], username, password)
    except:
        raise ValueError("Unable to obtain API key from program arguments or firewall.")


def main():

    #apikey = fetch_api_key()

    printdes("Example base script", o='printul')

    #######################
    #    Put code here    #
    #######################


if __name__ == '__main__':
    main()
