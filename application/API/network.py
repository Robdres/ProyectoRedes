import os
import subprocess 
import scapy.all as scapy
import nmap 
# We need to create regular expressions to ensure that the input is correctly formatted.
import re

def get_ipsubmask():
    ip_submasks = []
    data = subprocess.check_output(['ifconfig'])
    for i in data.split(b'\n'):
        if(b'inet' in i):
            for j in i.split(b' '):
                if re.match(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', j.decode()) and not j.startswith(b'255'):
                    aux = j.split(b'.')[:-1]
                    aux.append(b'0/24')
                    ip_submask = b''
                    for i in aux:
                        ip_submask+=i+b'.'
                    ip_submasks.append(ip_submask[:-1])
    return ip_submasks



def get_hosts(ip):
    # Scan for networks
    nm = nmap.PortScanner()
    nm.scan(hosts=ip, arguments='-sn')
    # Get a list of all hosts on the network
    hosts = nm.all_hosts()

    for i in hosts:
        print(nm[i])

get_hosts(get_ipsubmask()[1].decode())




