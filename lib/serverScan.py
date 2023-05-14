#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/3 17:22
# @Author  : name
# @File    : serverScan.py
import nmap

# openPortDict ==> {'127.0.0.1':[80,81,8080],}
def serverScan(openPortDict):
    """
    对所开放的端口进行服务及服务版本探测
    返回字典  {'127.0.0.1':[{'PORT':80,'SERVICE':'http','VERSION':'nginx 1.22.1'},],}
    :param openPortDict: ip的开放端口字典
    """
    portServerDcit = {}
    nmapIPList = []
    nmapPortList = []

    for (ip, portList) in openPortDict.items():
        nmapIPList.append(ip)
        for port in portList:
            nmapPortList.append(str(port).strip())

    '''
    nmapip nmap下ip参数,多个ip使用空格间隔
    nmapport nmap下port参数,多个port使用','(英文逗号)隔开
    '''
    nm = nmap.PortScanner()
    nmapip = ' '.join(nmapIPList)
    nmapport = ','.join(list(set(nmapPortList)))
    print('server scan...')
    nm.scan(hosts=nmapip, ports=nmapport, arguments='-v -Pn -sV')
    # print(nm.command_line())

    for host in nm.all_hosts():
        # 主机ip
        # print('Host:{} '.format(host))

        for proto in nm[host].all_protocols():
            # 获取ip下的所有端口
            portList = list(nm[host][proto].keys())
            portList.sort()
            for port in portList:
                # 信息提取，仅保留端口号、服务、服务版本
                if nm[host][proto][port]['state'] == 'open':
                    portDetailDict = {'PORT': port,
                                      'SERVICE': '{}'.format(nm[host][proto][port].get('name')),
                                      'VERSION': '{} {}'.format(nm[host][proto][port].get('product'),nm[host][proto][port].get('version'))}
                    portServerDcit.setdefault(host, []).append(portDetailDict)
                else:
                    pass

    return portServerDcit


# dd = {'121.5.110.219': [22, 80, 81, 8080], '175.178.253.93': [22, 80, 81, 8080]}
# portServerDcit = serverScan(dd)
# print(portServerDcit)