#!/usr/bin/python
# -*- coding: UTF-8 -*-
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
today = datetime.datetime.now().strftime('%Y%m%d')
yesterday = (datetime.datetime.now() + relativedelta(days=-1)).strftime("%Y%m%d")


def main():
    """主程序"""
    artWord = Figlet(font='slant')
    print('---------------------------------------------------------------')
    print(artWord.renderText('portMonitor'))
    print('---------------------------------------------------------------')

    emailText = ''
    # 端口扫描,{'127.0.0.1':[80,81,8080]}
    openPortDict = portScan()
    
    #print(openPortDict)

    # 服务扫描,{'127.0.0.1':[{'PORT':80,'SERVICE':'http','VERSION':'nginx 1.22.1'},],}
    portServerDict = serverScan(openPortDict)
    # portServerDict = {'121.5.110.219': [{'PORT': 22, 'SERVICE': 'ssh', 'VERSION': 'OpenSSH 8.2p1 Ubuntu 4ubuntu0.3'}, {'PORT': 80, 'SERVICE': 'http', 'VERSION': ' '}], '175.178.253.93': [{'PORT': 22, 'SERVICE': 'ssh', 'VERSION': 'OpenSSH 7.4'}, {'PORT': 80, 'SERVICE': 'http', 'VERSION': 'nginx '}]}

    # 字典转json  留存结果
    resultFileName = os.path.join(LogDirectory, '{}_scanResult.json')
    contentWrite(resultFileName.format(today),portServerDict)

    is_Monday = isMonday()
    if os.path.exists(resultFileName.format(yesterday)):
        todayFileName,yesterdayFileName = resultFileName.format(today),resultFileName.format(yesterday)
        changeDict = contentCheck(todayFileName,yesterdayFileName)

        if changeDict:
            '''
            addList: 较昨日新增的端口列表       
            reduceList: 较昨日关闭的端口列表
            '''
            addList, reduceList = changeDict['add'], changeDict['reduce']

            if len(addList) > 0 and len(reduceList) == 0:
                emailText = '[监测]-较昨日新增{}个端口\n{}'.format(len(addList), '\n'.join(addList))

            elif len(addList) == 0 and len(reduceList) > 0:
                emailText = '[监测]-较昨日关闭{}个端口\n{}'.format(len(reduceList), '\n'.join(reduceList))

            # 新增 关闭同时存在
            elif len(addList) > 0 and len(reduceList) > 0:
                emailText = '[监测]-较昨日新增{}个端口\n{}\n'.format(len(addList), '\n'.join(addList))
                emailText = emailText + '==================================\n'
                emailText = emailText + '[监测]-较昨日关闭{}个端口\n{}'.format(len(reduceList), '\n'.join(reduceList))

            else:
                pass

        elif not is_Monday:
            exit('[监测]-开放端口较昨日无变化')

    if is_Monday or not os.path.exists(resultFileName.format(yesterday)):
        todayContentList = []
        for ip in portServerDict.keys():
            todayContentList += ['{} {} {} {}'.format(ip, infoDict.get('PORT'), infoDict.get('SERVICE'), infoDict.get('VERSION')) for infoDict in portServerDict[ip]]
        emailText = emailText + '[监测]-总开放端口{}个(周一|周三|昨日无扫描时触发)\n{}'.format(len(todayContentList),'\n'.join(todayContentList))

    # print(emailText)
    if emailText:
        print('邮件内容:\n{}'.format(emailText))

        semail = sendemail()
        subject = '端口监测{}'.format(today)
        semail.send(subject, emailText)

    exit('finish')

if __name__ == "__main__":
    main()
