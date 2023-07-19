#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/3 17:22
# @Author  : name
# @File    : sendemail.py
import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser

RootPath = os.path.abspath('.')

class sendemail():
    def __init__(self, config_file_path=os.path.join(RootPath,'config.ini')):
        """get mail config values"""
        if config_file_path and os.path.exists(config_file_path):
            try:
                con = ConfigParser()
                con.read(config_file_path, encoding='utf-8')

                items = dict(con.items('email'))
                self.sender_maile = items.get('sender_maile')
                self.sender_pass = items.get('sender_pass')
                self.receive_maile = items.get('receive_maile')

            except Exception as e:
                exit('read config error: {}'.format(e))
        else:
            exit('config file not found')

    def send(self, subject, text, attachment_path=None):
        """
        email send fun
        :param subject: Theme
        :param text: body
        :param attachment_path: attachments,default null
        """
        global msg_root
        try:
            msg_root = MIMEMultipart('mixed')
            # Sender, receiver
            msg_root['From'] = '{}<{}>'.format(self.sender_maile, self.sender_maile)
            msg_root['To'] = self.receive_maile

            # Theme, text
            msg_root['subject'] = Header(subject, 'utf-8')
            text_sub = MIMEText(text, 'plain', 'utf-8')
            msg_root.attach(text_sub)
        except Exception as e:
            exit('Description Failed to write the email content: {}'.format(e))

        try:
            """Matches the SMTP server and port"""
            smtpServerDict = {
                'qq': {'smtpHost': 'smtp.qq.com', 'port': 25},
                '163': {'smtpHost': 'smtp.163.com', 'port': 25},
                '126': {'smtpHost': 'smtp.126.com', 'port': 25},
                'aliyun': {'smtpHost': 'smtp.aliyun.com', 'port': 25},
                'gmail': {'smtpHost': 'smtp.gmail.com', 'port': 587},
                '139': {'smtpHost': 'SMTP.139.com', 'port': 25},
            }

            identification = self.sender_maile.split('@')[-1].split('.')[0]
            smtpHost = smtpServerDict[identification]['smtpHost']
            smtpPort = smtpServerDict[identification]['port']

            smtp_obj = smtplib.SMTP()
            smtp_obj.connect(smtpHost, smtpPort)
            smtp_obj.login(self.sender_maile, self.sender_pass)
            smtp_obj.sendmail(self.sender_maile, self.receive_maile, msg_root.as_string())
            smtp_obj.quit()
            print('email sent successfully')

        except Exception as e:
            exit('email sent error:{}'.format(e))

# test
# semail = emailclass()
# subject = 'tile'
# text = 'body'
# semail.send(subject,text)
#
