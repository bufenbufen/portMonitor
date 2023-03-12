#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import datetime
from collections import Counter


def contentWrite(filename, value):
    """
    内容写入文件
    :param filename: 文件名
    :param value: 待写入值（列表或字符串）
    """

    # 存在相同文件名时，写入精确到秒的文件命名，如 scanresult2023_03_09_23_20_44.txt
    if os.path.exists(filename):
        filename = filename.split('.')
        filename = ''.join(filename[:-1]) + datetime.datetime.now().strftime('_%H_%M_%S') + '.' + filename[-1]

    dfile = open(filename, 'a', encoding='utf-8')
    if type(value).__name__ == 'list':
        for _value in value:
            dfile.write(_value + '\n')
    else:
        dfile.write(value + '\n')
    dfile.close()


def contentCheck(newFileName, oldFileName):
    """
    若两文件内容相同，返回False
    若当两文件内容不相同，返回提取变化值（字典格式，包含新增和减少项）
    :param newFileName: 今日生成的文件名
    :param oldFileName: 昨日生成的文件名
    """
    changeDict = {}
    addList = []
    reduceList = []

    newFile = open(newFileName, 'r', encoding='utf-8')
    oldFile = open(oldFileName, 'r', encoding='utf-8')

    # 去除换行符影响
    newContentList = [x.strip() for x in newFile.readlines()]
    oldContentList = [x.strip() for x in oldFile.readlines()]

    newFile.close()
    oldFile.close()

    if not Counter(newContentList) == Counter(oldContentList):
        """
        for循环1：提取较昨日 今日新增的端口
        for循环2：提取较昨日 今日关闭的端口
        """
        for newvalue in newContentList:
            if newvalue not in oldContentList:
                addList.append(newvalue)

        for oldvalue in oldContentList:
            if oldvalue not in newContentList:
                reduceList.append(oldvalue)

        changeDict['add'] = addList
        changeDict['reduce'] = reduceList
        return changeDict
    else:
        return False
