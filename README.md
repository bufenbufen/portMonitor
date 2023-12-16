#### portMonitor

portMonitor（端口监测），基于masscan实现，程序会每日对比上一日的端口情况，确认是否新增或关闭端口，后通过邮件下发监测情况，使用者可自定义每周几发送当日监测的全部端口至目标邮箱，且每日扫描情况会留痕保存。 
注：aliuyun默认23端口不开放，无法发送邮件



#### 1、环境配置

```
python模块安装
python3 -m pip install -r requirements.txt

文件权限
chmod 755 portMonitor -R

nmap安装
yum -y install nmap
apt-get -y install nmap
```



#### 2、配置文件config.ini

```
[email]
sender_maile = xxxxx@163.com      #发送方邮箱
sender_pass = xxxxxx			  #发送方SMTP授权码
receive_maile = xxxxx@163.com	  #接收方邮箱

[portrange]
range = 1-1000					  #扫描端口范围
```



#### 3、配置计划任务脚本start.sh

```
#!/usr/bin/bash
cd /root/portMonitor/              #portMonitor路径
/usr/bin/python3 portMonitor.py    #python路径，which python查看
```



#### 4、计划任务配置

```
crontab -e
30 6 * * * /root/portMonitor/start.sh 			#自定义计划任务执行时间，默认每天6点30分
```



### 扫描
![](https://github.com/bufenbufen/portMonitor/blob/master/images/0.png)




### 邮件
![](https://github.com/bufenbufen/portMonitor/blob/master/images/2.png)

