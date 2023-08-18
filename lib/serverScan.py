#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/3 17:22
# @Author  : name
# @File    : serverScan.py
import nmap

# openPortDict ==> {'127.0.0.1':[80,81,8080],}
def serverScan(openPortDict):
    """
    return  {'127.0.0.1':[{'PORT':80,'SERVICE':'http','VERSION':'nginx 1.22.1'},],}
    :param openPortDict: port dict
    """
    try:
        portServerDcit = {}
        nmapIPList = []
        nmapPortList = []

        for (ip, portList) in openPortDict.items():
            nmapIPList.append(ip)
            for port in portList:
                nmapPortList.append(str(port).strip())

        '''
        nmapip nmap ip arg,Multiple ip Spaces are separated
        nmapport nmap port arg,Multiple ports are separated by commas
        '''
        nmapip, nmapport = ' '.join(nmapIPList), ','.join(list(set(nmapPortList)))
        nm = nmap.PortScanner()
        nm.scan(hosts=nmapip, ports=nmapport, arguments='-v -Pn -sV')

        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                # Get the port under the ip address
                portList = list(nm[host][proto].keys())
                portList.sort()
                for port in portList:
                    # Extract the port number, service, and service version
                    if nm[host][proto][port]['state'] == 'open':
                        portDetailDict = {'PORT': port,
                                          'SERVICE': '{}'.format(nm[host][proto][port].get('name')),
                                          'VERSION': '{} {}'.format(nm[host][proto][port].get('product'),nm[host][proto][port].get('version'))}
                        portServerDcit.setdefault(host, []).append(portDetailDict)
                    else:
                        pass
    except KeyboardInterrupt:
        exit('ctrl-c end')
    except Exception as e:
        print('server scan:'+e)

    return portServerDcit

