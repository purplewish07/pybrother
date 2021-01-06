#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Date: 2021/01/06
# Author:   Shaun
# 檔案功能描述:
#   自動抓取機台狀態，更新資料庫，配合bash腳本，寫入系統排程crontab -e
# -------------------------------------------------------------------
import socket
# import pymysql
import os
import time
from datetime import datetime
# cnc_config = [('cnc27', "192.168.3.27"), ('cnc28', "192.168.3.28"), ('cnc29', "192.168.3.29"), ('cnc43', "192.168.3.43"),
# 			  ('cnc44', "192.168.3.44"), ('cnc45', "192.168.3.45"), ('cnc46', "192.168.3.46")]
# cnc_config = [('cnc27', "192.168.3.27"), ('cnc28', "192.168.3.28"), ('cnc29', "192.168.3.29"), ('cnc46', "192.168.3.46")]
cnc_config = [('cnc46', "192.168.3.46")]


def get_from_brother(ip='127.0.0.1', port=10000):
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.settimeout(10)
	try:
		client.connect((ip, port))
		# 取得工件數
		# instruct = '%CLOD    WKCNTR  ' + os.linesep + '00%'
		instruct = '%CLOD    WKCNTR  00\r\n%'
		# instruct = '%CLOD    PRD3    00\r\n%'
		# instruct = '%CIOCREF GRN     00\r\n%'
		client.send(instruct.encode())
		# lines = client.recv(3096).decode().split(os.linesep)
		lines = client.recv(1500).decode()
		# arr= [line.strip() for line in lines]
		# n=0
		# for e in arr:
		# 	v1=e.split(',')
		# 	if n>1:
		# 		# v1[1]=datetime.fromtimestamp(int(v1[1]) / 1e3)
		# 		v1[1]=datetime.fromtimestamp(int(v1[1]))
		# 		# date=v1[1]
		# 	n+=1
		# 	print(v1)
		# print(lines)
		# lines = client.recv(1024).decode()
		print(lines)
		lines = lines.split(os.linesep)
		lines = [line for line in lines if line.startswith('A01')]  # 選出以A01開頭的行
		fields = lines[0].split(',') # 拆分出字段，第3個字段就是目標[工件計數]
		parts = int(fields[2].strip())
		print('部品數量:',int(fields[2].strip()),'\n')
		# 取得狀態
		# instruct = '%CLOD    WKCNTR  00\r\n%'
		instruct = '%CLOD    PRD3    00\r\n%'
		client.sendall(instruct.encode())
		flag = True
		data=''
		while flag:
			lines = client.recv(1500).decode()
			# print('len:',len(lines),lines)
			data+=lines
			if lines[-1]=='%':
				flag = False
		log=data.split('\n')
		# print(data,'len:',len(data))
		for i in range(10):
			print(log[i])
		
		return parts
	except Exception as e:
		print(ip, e)
		return -1
	finally:
		client.close()


# def save_db(name='J44', qty=-1):
#     try:
#         conn = pymysql.Connect(user='root', password='1234', database='dademes', charset='utf8')
#         cus = conn.cursor()
#         if qty == -1:
#             cus.execute('update kbequipment set running=%s where name=%s', ('关机', name))
#         else:
#             cus.execute('update kbequipment set running=%s, status=%s where name=%s', ('正常', qty, name))
#         conn.commit()
#         cus.close()
#         conn.close()
#     except Exception as e:
#         print('机台号=%s保存数据异常,%s' % (name, e))

if __name__ == '__main__':
	try:
		for cnc_name, ip in cnc_config:
			print('正在讀取機台號=%s,ip=%s' % (cnc_name, ip))
			qty = get_from_brother(ip=ip)
			print(qty)
			# save_db(qty=qty, name=cnc_name)
	except Exception as e:
		print('__main__', e)
	finally:
		print('CNC數據讀取完畢... 30秒後再次讀取...')
		# time.sleep(10)
