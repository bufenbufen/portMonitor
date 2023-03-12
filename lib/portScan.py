#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import os
import json
from lib.getconfig import getconfig
from lib.contentDispose import contentWrite

RootPath = os.path.abspath('.')
LogDirectory = os.path.join(RootPath,'log')
today = datetime.datetime.now().strftime('%Y_%m_%d')

def portScan():
    """利用masscan执行端口扫描"""
    global today
    # masscan扫描结果
    scanResultList = []
    tmpFile = os.path.join(RootPath, 'tmp.json')
    if os.path.exists(tmpFile): os.remove(tmpFile)
    masscanPath, portRange = getconfig()
    targetipFile = os.path.join(RootPath, 'ip.txt')


    command = '{0} -iL {1} -p {2} -oJ {3} --rate 1000'.format(masscanPath, targetipFile, portRange, tmpFile)
    print('【command】 "{}"'.format(command))
    os.system(command)

    if os.path.exists(tmpFile):
        # 提取json文件中的端口
        with open(tmpFile, 'r') as f:
            for line in f:
                try:
                    if line.startswith('{ '):
                        line = line.replace('},', '}')
                        temp = json.loads(line)
                        temp1 = temp["ports"][0]
                        scanResultList.append(temp["ip"] + ':' + str(temp1["port"]))
                except Exception as e:
                    continue
            print('开放端口:\n'+'\n'.join(scanResultList))

        if os.path.exists(tmpFile):
            os.remove(tmpFile)
            pass
        else:
            pass
    else:
        print("扫描目标未发现端口开放")
    contentWrite(os.path.join(LogDirectory, 'scanresult{}.log'.format(today)), scanResultList)
    return scanResultList
