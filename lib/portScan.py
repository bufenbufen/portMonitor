#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import json
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
        with open(tmpFile, 'r') as f:
            for line in f:
                portList = []
                try:
                    if line.startswith('{ '):
                        line = line.replace('},', '}')
                        temp = json.loads(line)
                        temp1 = temp["ports"][0]
                        # scanResultList.append(temp["ip"] + ':' + str(temp1["port"]))
                        scanReusltDict.setdefault(temp["ip"],[]).append(temp1["port"])
                except Exception as e:
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
