#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/3 17:22
# @Author  : name
# @File    : portMonitor.py
import datetime
import os
from dateutil.relativedelta import relativedelta
from pyfiglet import Figlet
from lib.sendemail import sendemail
from lib.isMonday import isMonday
from lib.portScan import portScan
from lib.contentDispose import contentWrite,contentCheck
from lib.serverScan import serverScan

RootPath = os.path.abspath('.')
LogDirectory = os.path.join(RootPath,'log')
today, yesterday = datetime.datetime.now().strftime('%Y%m%d'), (datetime.datetime.now() + relativedelta(days=-1)).strftime("%Y%m%d")

def main():
    artWord = Figlet(font='slant')
    print('---------------------------------------------------------------')
    print(artWord.renderText('portMonitor'))
    print('---------------------------------------------------------------')

    emailText = ''
    # port scan, return {'127.0.0.1':[80,81,8080]}
    openPortDict = portScan()

    # server scan,return {'127.0.0.1':[{'PORT':80,'SERVICE':'http','VERSION':'nginx 1.22.1'},],}
    portServerDict = serverScan(openPortDict)

    # portServerDict = {'121.5.110.219': [{'PORT': 22, 'SERVICE': 'ssh', 'VERSION': 'OpenSSH 8.2p1 Ubuntu 4ubuntu0.3'}, {'PORT': 80, 'SERVICE': 'http', 'VERSION': ' '}], '175.178.253.93': [{'PORT': 22, 'SERVICE': 'ssh', 'VERSION': 'OpenSSH 7.4'}, {'PORT': 80, 'SERVICE': 'http', 'VERSION': 'nginx '}]}

    # dict to json, write file
    resultFileName = os.path.join(LogDirectory, '{}_scanResult.json')
    contentWrite(resultFileName.format(today),portServerDict)

    is_Monday = isMonday()

    if os.path.exists(resultFileName.format(yesterday)):
        # Changed data dictionary
        changeDict = contentCheck(resultFileName.format(today),resultFileName.format(yesterday))

        if changeDict:
            '''
            addList: compare the port list added yesterday
            reduceList: compare the port list that was reduced yesterday
            '''
            addList, reduceList = changeDict['add'], changeDict['reduce']

            # only add\only close\add and close
            if len(addList) > 0 and len(reduceList) == 0:
                emailText = '[monitor]-added {} ports\n{}'.format(len(addList), '\n'.join(addList))
            elif len(addList) == 0 and len(reduceList) > 0:
                emailText = '[monitor]-close {} ports\n{}'.format(len(reduceList), '\n'.join(reduceList))
            elif len(addList) > 0 and len(reduceList) > 0:
                emailText = '[monitor]-added {} ports\n{}\n==================================\n[monitor]-close {} ports\n{}'\
                    .format(len(addList), '\n'.join(addList), len(reduceList), '\n'.join(reduceList))
            else:
                pass
        elif not is_Monday: exit('no change in assets')

    if is_Monday or not os.path.exists(resultFileName.format(yesterday)):
        todayContentList = []
        for ip in portServerDict.keys():todayContentList += ['{} {} {} {}'.format(ip, infoDict.get('PORT'), infoDict.get('SERVICE'), infoDict.get('VERSION')) for infoDict in portServerDict[ip]]
        emailText = emailText + '[monitor]-total open {}\n{}'.format(len(todayContentList),'\n'.join(todayContentList))

    if emailText:
        print('email content:\n{}'.format(emailText))
        semail = sendemail()
        subject = 'port monitor{}'.format(today)
        semail.send(subject, emailText)

    exit('finish')

if __name__ == "__main__":
    main()
