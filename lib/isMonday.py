#!/usr/bin/python
# -*- coding: UTF-8 -*-
import calendar
import datetime


def isMonday():
    """判断周几，预期每周一 下发一次开放的全部端口"""

    currentDate = datetime.date.today()

    year = currentDate.year
    month = currentDate.month
    day = currentDate.day

    # print(calendar.weekday(year, month, day))
    currentDay = calendar.weekday(year, month, day)
    """
    currentday = 0 --> 星期一
    currentday = 2 --> 星期二
    currentday = 3 --> 星期三
    ...
    """

    if currentDay == 3:
        return True
    return False
