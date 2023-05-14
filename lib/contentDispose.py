#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import json

def contentWrite(filename, dictValue):
    """
    字典内容写入json
    :param filename: 文件名
    :param value: 待写入值（字典格式）
    """

    # 存在相同文件名时，文件名加入时间戳，如 <<20230504_1683201676.scanResult.json>>
    # if os.path.exists(filename):
    #     filename = filename.split(' ')
    #     filename = ''.join(filename[:-1]) + '_' + str(int(time.time())) + '.' + filename[-1]

    dfile = open(filename, 'w+', encoding='utf-8')
    if not type(dictValue).__name__ == 'dict':
        dictValue = json.dumps(dictValue)
        pass
    json.dump(dictValue, dfile, indent=2, sort_keys=True, ensure_ascii=False)

    if os.path.getsize(filename):
        os.remove(filename)
    dfile.close()


def contentCheck(fileNametoday, fileNameyesterday):
    """
    若两文件内容相同，返回False
    若当两文件内容不相同，返回提取变化值（字典格式，包含新增和减少项）
    :param fileNametoday: 今日生成的文件名
    :param fileNameyesterday: 昨日生成的文件名
    """
    changeDict = {}
    addList = []
    reduceList = []
    echoTemplate = '{} {} {} {}'

    filetoday = open(fileNametoday, 'r', encoding='utf-8')
    fileyesterday = open(fileNameyesterday, 'r', encoding='utf-8')

    todayContentDict = dict(json.load(filetoday))
    yesterdayContentDict = dict(json.load(fileyesterday))

    filetoday.close()
    fileyesterday.close()

    todayContentList = []
    for ip in todayContentDict.keys():
        todayContentList += [echoTemplate.format(ip,infoDict.get('PORT'),infoDict.get('SERVICE'),infoDict.get('VERSION')) for infoDict in todayContentDict[ip]]

    yesterdayContentList = []
    for ip in yesterdayContentDict.keys():
        yesterdayContentList += [echoTemplate.format(ip, infoDict.get('PORT'), infoDict.get('SERVICE'), infoDict.get('VERSION')) for
               infoDict in yesterdayContentDict[ip]]

    # 不相等
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
    今天和昨天都存在该ip，对比两个列表的端口开放情况，返回差异值（字典），changeDict('addList':xxx,'reduceList':xxx)
    :param todayList: ip地址
    :param todayList: 今日xx ip的开放端口列表，包含port、server、version
    :param yesterdayList: 昨日xx ip的开放端口列表，包含port、server、version
    """
    changeDict = {}
    addList = []
    reduceList = []
    echoTemplate = '{}  {}  {}  {}'

    if todayList and yesterdayList:
        todayPortList = [portINFO.get('PORT') for portINFO in todayList]
        yesterdayPortList = [portINFO.get('PORT') for portINFO in yesterdayList]

        addPortList = list(set(todayPortList) - set(yesterdayPortList))
        reducePortList = list(set(yesterdayPortList) - set(todayPortList))

        if set(todayPortList) == set(yesterdayPortList):
            return None

        if addPortList:
            for port in addPortList:
                # SERVICE = [portINFO.get('SERVICE') if portINFO.get('PORT') == port else None for portINFO in todayContentDict[ip]]
                # VERSION = [portINFO.get('VERSION') if portINFO.get('PORT') == port else None for portINFO in todayContentDict[ip]]

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
