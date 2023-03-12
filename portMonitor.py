#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import os
from dateutil.relativedelta import relativedelta
from lib.sendemail import sendemail
from lib.isMonday import isMonday
from lib.portScan import portScan
from lib.contentDispose import contentCheck


RootPath = os.path.abspath('.')
LogDirectory = os.path.join(RootPath,'log')
# 今日、昨日
today = datetime.datetime.now().strftime('%Y_%m_%d')
yesterday = (datetime.datetime.now() + relativedelta(days=-1)).strftime("%Y_%m_%d")


def main():
    """主程序"""
    global today, yesterday
    text = ''
    print('【{}】【端口扫描】'.format(today))
    scanResultList = portScan()

    is_monday = isMonday()

    if os.path.exists(os.path.join(LogDirectory,'scanresult{}.log'.format(yesterday))):
        todayFileName = os.path.join(LogDirectory, 'scanresult{}.log'.format(today))
        yesterdayFileName = os.path.join(LogDirectory,'scanresult{}.log'.format(yesterday))
        changeDict = contentCheck(todayFileName,yesterdayFileName)

        if changeDict:
            """
            :param addList: 今日新增的端口列表
            :param reduceList: 今日关闭的端口列表
            """
            addList = changeDict['add']
            reduceList = changeDict['reduce']

            if len(addList) > 0 and len(reduceList) == 0:
                text = '【--今日监测新增{}个端口--】\n{}'.format(len(addList),'\n'.join(addList))

            elif len(addList) == 0 and len(reduceList) > 0:
                text = '【--今日监测关闭{}个端口--】\n{}'.format(len(reduceList),'\n'.join(reduceList))

            # 新增 关闭同时存在
            elif len(addList) > 0 and len(reduceList) > 0:
                text = '【--今日监测新增{}个端口--】\n{}\n'.format(len(addList),'\n'.join(addList))
                text = text + '【--今日监测关闭{}个端口--】\n{}'.format(len(reduceList),'\n'.join(reduceList))

            else:
                pass

        elif not is_monday:
            exit('【--今日开放端口与昨日一致--】')


    if is_monday or not os.path.exists(os.path.join(LogDirectory,'scanresult{}.log'.format(yesterday))):
        text = text + '【--发现端口--】\n{}'.format('\n'.join(scanResultList))

    # print(text)
    if text:
        print('邮件内容:\n{}'.format(text))

        semail = sendemail()
        subject = '端口监测{}'.format(today)
        semail.send(subject, text)

    exit('程序结束')

if __name__ == "__main__":
    main()
