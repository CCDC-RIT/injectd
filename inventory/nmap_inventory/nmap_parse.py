"""
Author: Andrew

Description: uses nmap_python

Requirements: python-nmap package, ifaddr
"""

import nmap
import socket
import ifaddr

# Returns the best guess at the device's IP and netmask.
# Requires device to have a valid non-127 and non-169 IPv4 address active.
# May not work on devices with multiple valid IP addresses active (only first one will be returned)
def get_current_network_info():
    adapters = ifaddr.get_adapters()

    for adapter in adapters:
        for ip in adapter.ips:
            if ip.is_IPv4:
                if ip.ip.split(".")[0] != "127" and ip.ip.split(".")[0] != "169": #not routable so ignore
                    #return f"{ip}"
                    return f"{ip.ip}/{ip.network_prefix}"
                    """
                    return {
                        'interface': adapter.nice_name,
                        'ip': ip.ip,
                        'netmask': ip.network_prefix
                    }
                    """

def single_host(host_ip="127.0.0.1"):
    print(f"Starting single host scan of {host_ip}, this may take a minute...")
    nm = nmap.PortScanner()
    nm.scan(host_ip,arguments="-O") #'22-443'
    #nm.command_line() # nmap -oX - -p 22-443 -sV 127.0.0.1'
    return nm

def get_online_hosts(network_to_scan = get_current_network_info()):
    # we could prob just replace this with nm.scan() and then nm.all_hosts()
    nm = nmap.PortScanner()
    nm.scan(hosts=network_to_scan, arguments='-n -sP -PE -PA 20-500') #host identify up/down
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    online_hosts = []
    for host, status in hosts_list:
        #print('{0}:{1}'.host)
        if status == "up":
            online_hosts.append(host)
    return online_hosts

def network_scan(network_to_scan = get_current_network_info()):
    print(f"Starting network scan of {network_to_scan}, this may take a minute...")
    hosts = get_online_hosts(network_to_scan)
    nm = nmap.PortScanner()
    #nm.scan(hosts=network_to_scan, arguments='-n -sP -PE -PA 20-500') #host identify up/down
    for host_ip in hosts:
        nm.scan(host_ip,'22-1000')
    nm.scan(hosts,'22-1000')
    return nm

def export_to_file(portscanner,file = "nmap_results.csv"):
    file = file.replace("/","-") #sanitize
    #scanner = nmap.PortScanner()
    #scanner.scan(target, ports)
    with open(file, 'w') as file:
        file.write(portscanner.csv())
    print(f"Scan results saved to {file}")

    """
    host;protocol;port;name;state;product;extrainfo;reason;version;conf
    127.0.0.1;tcp;22;ssh;open;OpenSSH;protocol 2.0;syn-ack;5.9p1 Debian 5ubuntu1;10
    127.0.0.1;tcp;25;smtp;open;Exim smtpd;;syn-ack;4.76;10
    127.0.0.1;tcp;53;domain;open;dnsmasq;;syn-ack;2.59;10
    127.0.0.1;tcp;80;http;open;Apache httpd;(Ubuntu);syn-ack;2.2.22;10
    127.0.0.1;tcp;111;rpcbind;open;;;syn-ack;;10
    127.0.0.1;tcp;139;netbios-ssn;open;Samba smbd;workgroup: WORKGROUP;syn-ack;3.X;10
    127.0.0.1;tcp;443;;open;;;syn-ack;;
    """

def main():

    #single host example
    ip = "127.0.0.1"
    scanner = single_host(ip)
    print(scanner["osmatch"])
    #print(scanner.csv())
    #export_to_file(scanner,f"nmap_results_{ip}.csv")

    #network example
    #ip = get_current_network_info()
    #scanner = network_scan(ip)
    #print(scanner.csv())
    #export_to_file(scanner,f"nmap_results_{ip}.csv")

main()