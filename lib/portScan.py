#!/usr/bin/python
# -*- coding: UTF-8 -*
import os
import json
import re
from sys import platform
from lib.getconfig import getconfig

RootPath = os.path.abspath('.')

def portScan():
    """
    利用masscan执行端口扫描
    return scanReusltDict = {'127.0.0.1':[80,81,8080]}
    """
    scanReusltDict = {}
    # scanResultList = []
    tmpFile = os.path.join(RootPath, 'tmp.json')
    if os.path.exists(tmpFile): os.remove(tmpFile)
    masscanPath, portRange = getconfig()
    targetipFile = os.path.join(RootPath, 'ip.txt')

    command = '{0} -iL {1} -p {2} -oJ {3} --rate 1000'.format(masscanPath, targetipFile, portRange, tmpFile)
    print('command: "{}"'.format(command))
    os.system(command)

    if os.path.exists(tmpFile):
        # 提取json文件中的端口
        with open(tmpFile, 'r',encoding='utf-8') as f:
            for line in f.readlines():
                portList = []
                try:
                    ip = re.search('((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}',line)
                    port = re.search('port: (\d*),',line)
                    # print(ip.group(0)+':'+str(port.group(1)))
                    scanReusltDict.setdefault(ip.group(0),[]).append(port.group(1))
                except Exception as e:
                    print(e)
                    continue
            # print('开放端口:\n'+'\n'.join(scanResultList))
            # print('open port:\n\n{}'.format(scanReusltDict))

        if os.path.exists(tmpFile):
            os.remove(tmpFile)
            pass
        else:
            pass
    else:
        pass

    return scanReusltDict


