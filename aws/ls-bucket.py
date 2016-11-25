#!/usr/bin/python
# -*- coding: utf8 -*-
# 列出S3 的水桶名單
from boto.s3.connection import S3Connection
from os.path import expanduser 					# 匯入 “~” 家目錄解析模塊		
import argparse
parser = argparse.ArgumentParser(description = '抓取 Amazon AWS S3 buckets 資源列表.')
parser.add_argument('-i','--identity_file',  metavar='secret_file', type=str, help='指定 AWS credentials 檔案的位置', default= expanduser("~") + '/.aws/credentials')
args = parser.parse_args()

# 處理 credentials 設定值
home = expanduser("~")
import ConfigParser						# 匯入 配置檔 解析模塊
config = ConfigParser.ConfigParser()
config.read(args.identity_file)
aws_key_id  = config.get('default', 'aws_access_key_id')           #抓Access ID
aws_secret_id  = config.get('default', 'aws_secret_access_key')    #抓 Secret Key
# 正式開始 
conn = S3Connection(aws_key_id, aws_secret_id)

bucket = conn.get_all_buckets()

for b in bucket:
	print b.name