#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os.path
from configparser import ConfigParser

def getconfig():
    """
    返回配置文件中masscan路径、扫描端口范围
    widows   F:\a_tools\Information_collection\masscan\masscan.exe
    linux    /usr/bin/masscan
    portRange  1-65535
    """
    ConfigPath = os.path.join(os.path.abspath('.'), 'config.ini')
    con = ConfigParser()
    con.read(ConfigPath, encoding='utf-8')
    masscan = dict(con.items('masscan'))
    portrange = dict(con.items('portrange'))
    return masscan.get('path'), portrange.get('range')
