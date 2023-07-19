#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/3 17:22
# @Author  : name
# @File    : isMonday.py
import calendar
import datetime

def isMonday():
    """Determine whether it is Monday or Wednesday"""
    currentDate = datetime.date.today()

    year,month,day = currentDate.year,currentDate.month,currentDate.day
    currentDay = calendar.weekday(year, month, day)
    """
    currentday = 0 --> Monday
    currentday = 1 --> Tuesday
    currentday = 2 --> Wednesday
    ...
    """
    if currentDay == 0 or currentDay == 2:return True
    return False
