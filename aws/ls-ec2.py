#!/usr/bin/python
# -*- coding: utf8 -*-
# AWS EC2 列表成CSV   Marty Chao  20150908
# ~/.aws/credentials 要有AWS key and secret
#
# Arguments
from os.path import expanduser 					# 匯入 “~” 家目錄解析模塊
import argparse
parser = argparse.ArgumentParser(description = '抓取 Amazon AWS EC2 資源列表.')
parser.add_argument('-d','--debug',  help='顯示抓取region 的進度',action="store_true")
parser.add_argument('-i','--identity_file',  metavar='secret_file', type=str, help='指定 AWS credentials 檔案的位置', default= expanduser("~") + '/.aws/credentials')
parser.add_argument('-o','--output', help='output to file', default = 'EC2_list.csv' )
args = parser.parse_args()

# 處理 credentials 設定值
home = expanduser("~")
import ConfigParser						# 匯入 配置檔 解析模塊
config = ConfigParser.ConfigParser()
config.read(args.identity_file)
aws_key_id  = config.get('default', 'aws_access_key_id')           #抓Access ID
aws_secret_id  = config.get('default', 'aws_secret_access_key')    #抓 Secret Key
if args.debug :
	print args
	print (aws_key_id +":"+ aws_secret_id)
# 開始處理 EC2 List
import boto.ec2
regions = [ 'us-east-1','eu-west-1', 'us-west-1','us-west-2','ap-northeast-1','ap-southeast-1','ap-southeast-2','sa-east-1','eu-central-1']
inventory = []
for region in regions:
	conn = boto.ec2.connect_to_region(region,aws_access_key_id=aws_key_id,aws_secret_access_key=aws_secret_id)
	reserved_instances = conn.get_all_instances()
	if args.debug :
		print ('處理'+ region + '中....')
	instances = []
	for r_instance in reserved_instances:
		for instance in r_instance.instances:
			instances.append(instance)
	for i in  instances:
		host_info =  map(str,[i.id, i.ip_address,i.private_ip_address, i.instance_type,
				 i.region.name, i.state, i.key_name, i.public_dns_name, i.placement,
				 i.architecture])
		inventory.append(host_info)
import csv
if not args.debug :
	print args.output
	with open(args.output, "wb") as f:
		writer = csv.writer(f)
		writer.writerows(inventory)
elif args.debug:
	with open("/dev/stdout", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(inventory)
