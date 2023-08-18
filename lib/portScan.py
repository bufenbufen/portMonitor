# -*- coding: utf-8 -*-
# @Time    : 2023/5/3 17:22
# @Author  : name
# @File    : portScan.py
import os
import re
import platform
from lib.getconfig import getconfig

RootPath = os.path.abspath('.')

def portScan():
    """
    masscan scan port
    return scanReusltDict = {'127.0.0.1':[80,81,8080]}
    """
    try:
        scanReusltDict = {}
        tmpFile = os.path.join(RootPath, 'tmp.json')

        # delete tmp file
        if os.path.exists(tmpFile): os.remove(tmpFile)

        plat = platform.system().lower()

        if plat == 'windows':masscanPath = os.path.join(RootPath,'bin','masscan.exe')
        elif plat == 'linux':masscanPath = os.path.join(RootPath,'bin','masscan')
        else:exit()

        portRange = getconfig()
        targetipFile = os.path.join(RootPath, 'ip.txt')

        command = '{0} -iL {1} -p {2} -oJ {3} --rate 1000'.format(masscanPath, targetipFile, portRange, tmpFile)
        print('command: "{}"'.format(command))
        os.system(command)

        if os.path.exists(tmpFile):
            # Extract ports from json
            with open(tmpFile, 'r',encoding='utf-8') as f:
                for line in f.readlines():
                    try:
                        ip = re.search('((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}',line)
                        port = re.search('port: (\d*),',line)
                        scanReusltDict.setdefault(ip.group(0),[]).append(port.group(1))
                    except Exception as e:
                        # print(e)
                        continue

            if os.path.exists(tmpFile):
                os.remove(tmpFile)
                pass
            else:
                pass
        else:
            pass
    except KeyboardInterrupt:
        exit('ctrl-c end')
    except Exception as e:
        exit('port scan'+e)

    return scanReusltDict


