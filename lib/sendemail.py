#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser

RootPath = os.path.abspath('.')

class sendemail():
    """邮件发送类"""

    def __init__(self, config_file_path=os.path.join(RootPath,'config.ini')):
        """
        构造, 配置文件提取邮箱凭证
        :param config_file_path: 配置文件路径，默认为主程序下config.ini
        """
        if config_file_path and os.path.exists(config_file_path):
            try:
                con = ConfigParser()
                con.read(config_file_path, encoding='utf-8')

                items = dict(con.items('email'))
                self.sender_maile = items.get('sender_maile')
                self.sender_pass = items.get('sender_pass')
                self.receive_maile = items.get('receive_maile')

            except Exception as e:
                exit('配置文件读取错误：{}'.format(e))
        else:
            exit('配置文件不存在')

    def send(self, subject, text, attachment_path=None):
        """
        发送邮件
        :param subject: 邮件标题（主题）
        :param text: 邮件正文
        :param attachment_path: 附件，默认为空
        """
        global msg_root
        try:
            msg_root = MIMEMultipart('mixed')
            # 发送方、接收方
            msg_root['From'] = '{}<{}>'.format(self.sender_maile, self.sender_pass)
            msg_root['To'] = self.receive_maile

            # 主题、文本
            msg_root['subject'] = Header(subject, 'utf-8')
            text_sub = MIMEText(text, 'plain', 'utf-8')
            msg_root.attach(text_sub)
        except Exception as e:
            exit('邮件内容写入失败:{}'.format(e))

        try:
            """
            邮件发送
            根据配置文件中发送者邮箱后缀匹配SMTP服务器及端口
            """
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
            # print(smtpHost,'type:',type(smtpHost),smtpPort,'type:',type(smtpPort))

            smtp_obj = smtplib.SMTP()
            smtp_obj.connect(smtpHost, smtpPort)
            smtp_obj.login(self.sender_maile, self.sender_pass)
            smtp_obj.sendmail(self.sender_maile, self.receive_maile, msg_root.as_string())
            smtp_obj.quit()
            print('邮件发送成功')

        except Exception as e:
            exit('邮件发送错误:{}'.format(e))

# 邮件主题
# semail = emailclass()
# subject = 'tile'
# text = 'body'
# semail.send(subject,text)
#
