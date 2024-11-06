"""
Author: Andrew

Description: uses nmap_python

Requirements: python-nmap package
"""

import nmap

def single_host(host_ip):
    nm = nmap.PortScanner()
    nm.scan(host_ip,'22-443') #'22-443'
    #nm.command_line() # nmap -oX - -p 22-443 -sV 127.0.0.1'
    return nm

def network_scan():
    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.1.0/24', arguments='-n -sP -PE -PA21,23,80,3389')
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    for host, status in hosts_list:
        print('{0}:{1}'.host)

def export_to_file(portscanner,file = 'nmap_results.csv'):
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
    print("Starting")
    scanner = single_host("127.0.0.1")
    print(scanner.csv())

main()