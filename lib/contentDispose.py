# -*- coding: utf-8 -*-
# @Time    : 2023/5/3 17:22
# @Author  : name
# @File    : contenDispose.py
import os
import json
import time

def contentWrite(filename, dictValue):
    """
    dict -> json
    :param filename: write file name
    :param dictValue: write value
    """
    # Same file name, add timestamp, example <<20230504_1683201676.scanResult.json>>
    if os.path.exists(filename):
        filename = filename.split('_')
        filename = ''.join(filename[:-1]) + '_' + str(int(time.time())) + '.' + filename[-1]

    dfile = open(filename, 'w+', encoding='utf-8')
    if not type(dictValue).__name__ == 'dict': dictValue = json.dumps(dictValue)
    json.dump(dictValue, dfile, indent=2, sort_keys=True, ensure_ascii=False)

    if os.path.getsize(filename): os.remove(filename)
    dfile.close()


def contentCheck(fileNametoday, fileNameyesterday):
    """
    The file same content,return False
    The file content is different, return difference
    :param fileNametoday: Today file name
    :param fileNameyesterday: Yesterday file name
    """
    changeDict = {}
    addList, reduceList = [],[]

    filetoday = open(fileNametoday, 'r', encoding='utf-8')
    fileyesterday = open(fileNameyesterday, 'r', encoding='utf-8')

    todayContentDict = dict(json.load(filetoday))
    yesterdayContentDict = dict(json.load(fileyesterday))

    filetoday.close()
    fileyesterday.close()

    echoTemplate = '{} {} {} {}'
    todayContentList = []
    for ip in todayContentDict.keys():
        todayContentList += [echoTemplate.format(ip,infoDict.get('PORT'),infoDict.get('SERVICE'),infoDict.get('VERSION')) for infoDict in todayContentDict[ip]]

    yesterdayContentList = []
    for ip in yesterdayContentDict.keys():
        yesterdayContentList += [echoTemplate.format(ip, infoDict.get('PORT'), infoDict.get('SERVICE'), infoDict.get('VERSION')) for
               infoDict in yesterdayContentDict[ip]]

    if not todayContentDict == yesterdayContentDict:
        todayInfoList = [':'.join(todayInfo.rstrip().split(' ')[:2]) for todayInfo in todayContentList]
        yesterdayInfoList = [':'.join(yesterdayInfo.rstrip().split(' ')[:2]) for yesterdayInfo in yesterdayContentList]

        for todayInfo in todayContentList:
            todayInfo_ip_port = ':'.join(todayInfo.rstrip().split(' ')[:2])
            if todayInfo_ip_port not in yesterdayInfoList:
                addList.append(todayInfo.rstrip())

        for yesterdayInfo in yesterdayContentList:
            yesterInfo_ip_port = ':'.join(yesterdayInfo.rstrip().split(' ')[:2])
            if yesterInfo_ip_port not in todayInfoList:
                reduceList.append(yesterdayInfo.rstrip())

    else:
        return False

    changeDict['add'] = addList
    changeDict['reduce'] = reduceList
    return changeDict


def checkPortList(ip, todayList=None, yesterdayList=None):
    """
    With ip, compare the last two days open port, return changeDict('addList':xxx,'reduceList':xxx)
    :param ip: ip
    :param todayList: xx ip open list today
    :param yesterdayList: xx ip open list yesterday
    """
    changeDict = {}
    addList,reduceList = [],[]

    echoTemplate = '{}  {}  {}  {}'
    if todayList and yesterdayList:
        todayPortList = [portINFO.get('PORT') for portINFO in todayList]
        yesterdayPortList = [portINFO.get('PORT') for portINFO in yesterdayList]

        addPortList = list(set(todayPortList) - set(yesterdayPortList))
        reducePortList = list(set(yesterdayPortList) - set(todayPortList))

        if set(todayPortList) == set(yesterdayPortList):return None

        if addPortList:
            for port in addPortList:
                SERVICE = [portINFO.get('SERVICE') for portINFO in todayList if portINFO.get('PORT') == port][0]
                VERSION = [portINFO.get('VERSION') for portINFO in todayList if portINFO.get('PORT') == port][0]
                if not SERVICE: SERVICE = None
                if not VERSION: VERSION = None

                addList.append(echoTemplate.format(ip, port, SERVICE, VERSION))
                print('add:' + echoTemplate.format(ip, port, SERVICE, VERSION))

        if reducePortList:
            for port in reducePortList:
                SERVICE = [portINFO.get('SERVICE') for portINFO in yesterdayList if portINFO.get('PORT') == port][0]
                VERSION = [portINFO.get('VERSION') for portINFO in yesterdayList if portINFO.get('PORT') == port][0]
                if not SERVICE: SERVICE = None
                if not VERSION: VERSION = None

                reduceList.append(echoTemplate.format(ip, port, SERVICE, VERSION))
                print('del:' + echoTemplate.format(ip, port, SERVICE, VERSION))

    elif todayList and not yesterdayList:
        pass

    elif not todayList and yesterdayList:
        pass

    changeDict['addList'] = addList
    changeDict['reduceList'] = reduceList
    return changeDict
