#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/3 17:22
# @Author  : name
# @File    : getconfig.py
import os.path
from configparser import ConfigParser

def getconfig():
    """
    Return the masscan path and port range of the configuration file
    widows   F:\a_tools\Information_collection\masscan\masscan.exe
    linux    /usr/bin/masscan
    portRange  1-65535
    """
    ConfigPath = os.path.join(os.path.abspath('.'), 'config.ini')
    con = ConfigParser()
    con.read(ConfigPath, encoding='utf-8')
    return dict(con.items('portrange')).get('range')
