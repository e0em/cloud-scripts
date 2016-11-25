#!/usr/bin/python
# -*- coding: utf8 -*- 
# AWS 每日帳單抓取程序 Marty Chao 20150908 
import boto
import boto.ec2
import boto.ec2.cloudwatch
import sys
import argparse
import datetime
from pprint import pprint

def exit_with_error(msg):
	"""
	Write an error message to STDERR and
	exit with exitstatus 1.
	"""
	sys.stderr.write("Errorn" % msg)
	sys.stderr.flush()
	sys.exit(1)

def date(date_string):
	"""
	Validating and converting a string presenting a date
	into a datetime object.
	Accepted formats: dd/mm/yyyy, dd/mm/yy
	Smart values: today, yesterday
	"""
	date_object = None
	if date_string == 'today':
		now = datetime.datetime.now()
		return datetime.datetime(now.year, now.month, now.day)
	elif date_string == 'yesterday':
		yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
		return datetime.datetime(yesterday.year, yesterday.month, yesterday.day)
	accepted_date_formats = ['%d/%m/%Y', '%d/%m/%y','%Y-%m-%d']
	for date_format in accepted_date_formats:
		try:
			date_object = datetime.datetime.strptime(date_string, date_format)
			#pprint(date_object)
			return date_object
		except ValueError as ve:
			pass
	raise ValueError('Entered date is not in accepted format.')

def get_metric(date, metrics):
	"""
	通過抓去前兩天資料相減取得一日費用
	return 值: dict 字典格式 費用名稱 as key and the value.
	"""
	stats = {}
	start = date - datetime.timedelta(hours=18)
	#print 'Retrieving statistics from %s to %s.\n' % (start, date)
	for metric in metrics:
		if u'ServiceName' in metric.dimensions:
			datapoints = metric.query(start, date, 'Maximum')
			#print datapoints
			datapoints = sorted(datapoints, key=lambda datapoint: datapoint[u'Timestamp'], reverse=True)
			stats[metric.dimensions[u'ServiceName'][0]] = (datapoints[0])[u'Maximum']
	return stats

# 計費資料只有在US-East-1 region.
region_name = 'us-east-1'

if __name__ == '__main__':
	# Arguments
	parser = argparse.ArgumentParser(description = '抓取AWS 帳單資料.')
	# 如果沒設定時間，默認抓取昨天的帳單.
	yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
	parser.add_argument('-d', '--date', metavar='date', type=date, help='設定抓取的日期，沒設定默認昨天。', default=datetime.datetime(yesterday.year, yesterday.month, yesterday.day))
	parser.add_argument('-m', '--metric', metavar='metric', help='抓取單一值 for zabbix 使用，支持的參數有 EC2|DataTransfer|kms|SNS|S3|SQS')
	args = parser.parse_args()

	# 鏈接到 cloudwatch endpoint
	conn = boto.ec2.cloudwatch.connect_to_region(region_name)
	if conn == None:
		exit_with_error('無法連線到指定區域 region %s' % region_name)

	# 抓取相關參數 metrics	
	billing_metrics = conn.list_metrics(metric_name=u'EstimatedCharges', namespace=u'AWS/Billing')

	# Get the data for the relevant metrics at the beginning of the day and at the end.
	test_avg = get_metric(args.date, billing_metrics)
	metric_data = {}
	metric_data['begin_of_day'] = get_metric(args.date, billing_metrics)
	now = datetime.datetime.now()
	# 設定今天的時間參數到 『today』
	today = datetime.datetime(now.year,now.month,now.day)
	if args.metric is None:
		print (str(now.year)+'年'+str(now.month)+"月"+ str(now.day-1)+"日 AWS費用")
		print '================================'
	if today != args.date:
		metric_data['end_of_day'] = get_metric(args.date + datetime.timedelta(days=1), billing_metrics)
	else:
		metric_data['end_of_day'] = get_metric(now, billing_metrics)
	# 正式來抓資料 放在 charges字典 裏面	
	charges = {}
	for metric_name in metric_data['end_of_day']:
		charges[metric_name] = metric_data['end_of_day'][metric_name] - metric_data['begin_of_day'][metric_name]
		if args.metric is None:
			print '%-20s: %.2f USD' % (metric_name, charges[metric_name])
	print charges
	# 如果命令行參數有 --metric 相應的output如下
	if args.metric == 'EC2':
		print charges['AmazonEC2']
	elif args.metric == 'DataTransfer' :
		print charges['AWSDataTransfer']
	elif args.metric == 'kms':
		print charges['awskms']
	elif args.metric == 'SNS':
		print charges['AmazonSNS']
	elif args.metric == 'S3':
		print charges['AmazonS3']
	elif args.metric == 'SQS':
		print charges['AWSQueueService']
