#!/usr/bin/python
# -*- coding: utf8 -*-
# ~/.aws/credentials 要有AWS key and secret
#
# 處理 credentials 設定值
from os.path import expanduser 					# 匯入 “~” 家目錄解析模塊
home = expanduser("~")
import ConfigParser						# 匯入 配置檔 解析模塊
config = ConfigParser.ConfigParser()
config.read(home +'/.aws/credentials')
aws_key_id  = config.get('default', 'aws_access_key_id')           #抓Access ID
aws_secret_id  = config.get('default', 'aws_secret_access_key')    #抓 Secret Key
# print (aws_key_id +":"+ aws_secret_id)
