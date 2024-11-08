"""
Author: Andrew

Description: uses nmap_python

Requirements: python-nmap package, ifaddr
"""

import nmap
import socket
import ifaddr
import csv

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
    print(f"Online hosts: {online_hosts}")
    return online_hosts

# Scans the specified subnet. Returns PortScanner() object with scan results.
def network_scan(network_to_scan = get_current_network_info()):
    print(f"Starting network scan of {network_to_scan}, this may take a minute...")
    #hosts = get_online_hosts(network_to_scan)
    nm = nmap.PortScanner()
    #nm.scan(hosts=network_to_scan, arguments='-n -sP -PE -PA 20-500') #host identify up/down
    #for host_ip in hosts:
        #nm.scan(host_ip,'22-1000')
    #nm.scan(hosts=network_to_scan,arguments="-sS -sU -O -sV -T4 -Pn --open")
    nm.scan(hosts=network_to_scan,arguments="-sS -sU -O -sV -T5 -Pn --open -p 1-1000") #faster
    """
    -sS: Performs a TCP SYN scan to check for open TCP ports.
    -sU: Performs a UDP scan to check for open UDP ports.
    -O: Enables OS detection to determine the operating system and version.
    -sV: Enables service version detection to identify the version of services running on each open port.
    -T4: Sets the timing template to speed up the scan (1 is slowest, 5 is fastest). T4 is a good balance between speed and accuracy.
    -Pn: Disables pinging hosts to treat all IPs as alive, useful for networks where ICMP is blocked.
    """
    return nm

# Given a portscanner object, parse the results into a dictionary with main key of the IP address of a host which corresponds to a sub-dictionary containing all the other info
def parse_portscanner(nm):
    """
    {
        "192.168.1.1": {
            "ip_address": "192.168.1.1",
            "hostname": "example-hostname",
            "os": [
                {"os_family": "Linux", "os_gen": "5", "accuracy": "98"},
                # ... additional OS classes if available
            ],
            "ports": [
                {
                    "protocol": "tcp",
                    "port": 80,
                    "state": "open",
                    "service": "http",
                    "version": "Apache httpd 2.4.29",
                    "product": "Apache",
                    "extra_info": "Debian"
                },
                # ... more ports as discovered
            ]
        },
        # ... more hosts
    }
    """
    scan_results = dict()
    for host in nm.all_hosts():
        host_info = {
            "ip_address": host,
            "hostname": nm[host].hostname(),
            "os": [],
            "ports": []
        }
        
        # Add OS information if available
        if 'osclass' in nm[host]:
            for os in nm[host]['osclass']:
                host_info["os"].append({
                    "os_family": os.get("osfamily"),
                    "os_gen": os.get("osgen"),
                    "accuracy": os.get("accuracy")
                })
        
        # Loop through all scanned protocols (tcp/udp)
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            for port in ports:
                port_info = nm[host][proto][port]
                host_info["ports"].append({
                    "protocol": proto,
                    "port": port,
                    "state": port_info["state"],
                    "service": port_info["name"],
                    "version": port_info.get("version", ""),
                    "product": port_info.get("product", ""),
                    "extra_info": port_info.get("extrainfo", "")
                })
        
        # Add host information to the main results dictionary
        scan_results[host] = host_info
    
    return scan_results

# Given the dict from parse_portscanner(), write it as a CSV to a file.
def export_dict_to_file(scan_results, file="nmap_results.csv"):
    file = file.replace("/","-") #sanitize if called with subnet mask
    # Define the headers for the CSV file
    headers = [
        "IP Address", "Hostname", "OS Family", "OS Gen", "OS Accuracy", 
        "Protocol", "Port", "State", "Service", "Version", "Product", "Extra Info"
    ]
    
    # Open a new CSV file for writing
    with open(file, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        
        # Write the headers to the CSV file
        writer.writerow(headers)
        
        # Iterate through the scan results and write each entry to the CSV
        for host, host_info in scan_results.items():
            ip_address = host_info["ip_address"]
            hostname = host_info["hostname"]
            
            # Handle OS information (may have multiple OS entries)
            if host_info["os"]:
                #for os_info in host_info["os"]:
                os_family = host_info["os"].get("os_family", "")
                os_gen = host_info["os"].get("os_gen", "")
                os_accuracy = host_info["os"].get("accuracy", "")
                
                # Iterate over each port for this host and OS combination
                if host_info["ports"]:
                    for port_info in host_info["ports"]:
                        row = [
                            ip_address,
                            hostname,
                            os_family,
                            os_gen,
                            os_accuracy,
                            port_info["protocol"],
                            port_info["port"],
                            port_info["state"],
                            port_info["service"],
                            port_info.get("version", ""),
                            port_info.get("product", ""),
                            port_info.get("extra_info", "")
                        ]
                        writer.writerow(row)
                else:
                    # If no ports, write OS information alone
                    writer.writerow([
                        ip_address, hostname, os_family, os_gen, os_accuracy, 
                        "", "", "", "", "", "", ""
                    ])
            else:
                # Handle case with no OS information but has port information
                for port_info in host_info["ports"]:
                    row = [
                        ip_address,
                        hostname,
                        "",
                        "",
                        "",
                        port_info["protocol"],
                        port_info["port"],
                        port_info["state"],
                        port_info["service"],
                        port_info.get("version", ""),
                        port_info.get("product", ""),
                        port_info.get("extra_info", "")
                    ]
                    writer.writerow(row)

def export_to_file(portscanner,file = "nmap_results.csv"):
    file = file.replace("/","-") #sanitize if called with subnet mask
    #scanner = nmap.PortScanner()
    #scanner.scan(target, ports)
    with open(file, 'w') as file:
        file.write(portscanner.csv())
    print(f"Scan results saved to {file}")

    """
    host;hostname;protocol;port;name;state;serviceversion;product;ostype;osvendor;osfamily;osgen;osaccuracy

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
    # 
    #ames': [{'name': 'localhost', 'type': 'PTR'}], 'addresses': {'ipv4': '127.0.0.1'}, 'vendor': {}, 'status': {'state': 'up', 'reason': 'localhost-response'}, 'uptime': {'seconds': '689828', 'lastboot': 'Wed Oct 30 22:23:03 2024'}, 'tcp': {631: {'state': 'open', 'reason': 'syn-ack', 'name': 'ipp', 'product': '', 'version': '', 'extrainfo': '', 'conf': '3', 'cpe': ''}}, 'portused': [{'state': 'open', 'proto': 'tcp', 'portid': '631'}, {'state': 'closed', 'proto': 'tcp', 'portid': '1'}, {'state': 'closed', 'proto': 'udp', 'portid': '42086'}], 'osmatch': [{'name': 'Linux 2.6.32', 'accuracy': '100', 'line': '55543', 'osclass': [{'type': 'general purpose', 'vendor': 'Linux', 'osfamily': 'Linux', 'osgen': '2.6.X', 'accuracy': '100', 'cpe': ['cpe:/o:linux:linux_kernel:2.6.32']}]}]}
    """
    nm = nmap.PortScanner()
    nm.scan("127.0.0.1", arguments="-O")
    if 'osclass' in nm['127.0.0.1']:
        for osclass in nm['127.0.0.1']['osclass']:
            print('OsClass.type : {0}'.format(osclass['type']))
            print('OsClass.vendor : {0}'.format(osclass['vendor']))
            print('OsClass.osfamily : {0}'.format(osclass['osfamily']))
            print('OsClass.osgen : {0}'.format(osclass['osgen']))
            print('OsClass.accuracy : {0}'.format(osclass['accuracy']))
            print('')
    print("A")
    """

    #single host example
    #ip = "127.0.0.1"
    #scanner = single_host(ip)
    #print(scanner["osmatch"])
    #print(scanner.csv())
    #export_to_file(scanner,f"nmap_results_{ip}.csv")

    #hybrid
    ip = "127.0.0.1"
    scanner = network_scan(ip)
    results_dict = parse_portscanner(scanner)
    export_dict_to_file(results_dict,f"nmap_results_{ip}.csv")

    #network example
    #ip = get_current_network_info()
    ip = "10.0.10.0/24"
    #scanner = network_scan(ip)
    #print(scanner.csv())
    #export_to_file(scanner,f"nmap_results_{ip}.csv")
    results_dict = parse_portscanner(scanner)
    export_dict_to_file(results_dict,f"nmap_results_{ip}.csv")

main()
