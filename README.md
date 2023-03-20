# portMonitor

portMonitor（端口监测），基于masscan实现，程序功能如下：
```
1、每周一将当日监测的全部端口至目标邮箱
2、每日对比上一日的端口情况，判断端口新增、关闭情况，若开放端口存在变动，邮件下发变动详情
3、每日扫描留痕保存
```


### 1、python模块及masscan安装

```
pip install -r requirements.txt
或 python -m pip install -r requirements.txt

# 安装masscan
ubuntu: apt-get install masscan -y
centos: yum install masscan -y
```



### 2、配置文件config.ini

```
[email]
sender_maile = xxxxx@163.com      #发送方邮箱
sender_pass = xxxxxx			#发送方SMTP授权码
receive_maile = xxxxx@163.com	    #接收方邮箱

[masscan]
path = /usr/bin/masscan		#masscan路径，which masscan查看

[portrange]
range = 1-1000		 #扫描端口范围
```



### 3、配置计划任务脚本start.sh，计划任务直接执行python无结果（疑惑）

```
#!/usr/bin/bash
cd /root/portMonitor/              #portMonitor路径
/usr/bin/python3 portMonitor.py    #python路径，which python查看
```



### 4、计划任务配置

```
crontab -e
30 6 * * * /root/portMonitor/start.sh 			#自定义计划任务执行时间，默认每天6点30分
```



### 单次扫描
![](https://github.com/bufenbufen/portMonitor/blob/master/images/1.png)




### 邮件
![](https://github.com/bufenbufen/portMonitor/blob/master/images/3.png)

