import subprocess 
import nmap 
import re
#import arpSpoof as spoof

class Network():
    def get_ipsubmask(self):
        ip_submasks = []
        data = subprocess.check_output(['ifconfig'])
        for k in data.split(b'\n\n'):
            aux1 = {}
            for i in k.split(b'\n'):
                #check mask
                if(b'inet ' in i):
                    for j in i.split(b' '):
                        if re.match(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', j.decode()) and not j.startswith(b'255'):
                            aux = j.split(b'.')[:-1]
                            aux.append(b'0/24')
                            ip_submask = b''
                            for i in aux:
                                ip_submask+=i+b'.'
                            aux1['ipv4'] = (ip_submask[:-1])
                #check mac
                if(b'ether' in i):
                    for j in i.split(b' '):
                        if re.match(r'^[a-fA-F0-9]{2}(:[a-fA-F0-9]{2}){5}$', j.decode()):
                            aux1['mac'] = j
                if(len(aux1)!=0):
                    ip_submasks.append(aux1)
        holder = []
        aux = False
        for i in ip_submasks:
            if (len(i)==2):
                for j in holder:
                    if i['ipv4'] == j['ipv4']:
                        aux = True
                if(aux):
                    continue
                holder.append(i)
        print(holder)
        return holder


    #function to get connected devices
    def get_hosts(self):
        a_host = self.get_ipsubmask()[0]
        # Scan for networks
        result_hosts = []
        nm = nmap.PortScanner()
        nm.scan(hosts=a_host['ipv4'].decode(), arguments='-sn')

        # Get a list of all hosts on the network
        hosts = nm.all_hosts()
        
        for i in hosts:
            host = []
            host.append(nm[i]['addresses']['ipv4'].split('.')[-1])
            if('mac' in (nm[i]['addresses'])):
                host.append(nm[i]['addresses']['mac'])
            else:
                host.append(a_host['mac'])
            host.append(nm[i]['status']['state'])
            result_hosts.append(host)
        return result_hosts

    #Function ot get information
    def get_os(self, ipv4):
        nm = nmap.PortScanner()
        nm.scan(hosts = ipv4.decode(),arguments="-O")
        hosts = nm.all_hosts()
        oss = []
        for i in hosts:
            for j in nm[i]['osmatch']:
                os = []
                os.append(j['name'])
                os.append(j['accuracy'])
                oss.append(os)
        return oss

    def get_gateway(self):
        data = subprocess.check_output(['arp','-a'])
        ip = None
        for i in data.split(b'\n'):
            if(b'gateway' in i):
                ip = i.split(b" ")[1][1:-1]
        return ip

    def get_hosts_limits(self):
        data = subprocess.check_output(['sh','./get_host.sh'])
        data_1 = []
        for i in data.split(b'(Main) >>> ')[-2:-1]:
            for j in i.split(b'\n')[2:-2]:
                aux = []
                for k in j.split(b'\x1b')[2:]:
                    if k!=b'(0x' and k!=b'(B':
                        aux.append(k[3:].strip())
                if len(aux) != 0:
                    data_1.append(aux)
        return data_1


model = Network()
print(model.get_os(b"192.168.68.109"))