#!/usr/local/bin/python3
import boto3
import datetime

s3 = boto3.resource('s3')
cloudwatch = boto3.client('cloudwatch')

now = datetime.datetime.now()
for bucket in s3.buckets.all():
	bucket_size = None
	bucket_count = None
	cloudwatch_size = cloudwatch.get_metric_statistics(
		Namespace='AWS/S3',
		MetricName='BucketSizeBytes',
		Dimensions=[
			{'Name': 'BucketName', 'Value': bucket.name},
			{'Name': 'StorageType', 'Value': 'StandardStorage'}
		],
		Statistics=['Maximum'],
		Period=86400,
		StartTime=(now - datetime.timedelta(days=1)).isoformat(),
		EndTime=now.isoformat()
	)

	cloudwatch_count = cloudwatch.get_metric_statistics(
		Namespace='AWS/S3',
		MetricName='NumberOfObjects',
		Dimensions=[
			{'Name': 'BucketName', 'Value': bucket.name},
			{'Name': 'StorageType', 'Value': 'AllStorageTypes'}
		],
		Statistics=['Maximum'],
		Period=86400,
		StartTime=(now - datetime.timedelta(days=1)).isoformat(),
		EndTime=now.isoformat()
	)

	if cloudwatch_size["Datapoints"]:
		bucket_size = cloudwatch_size["Datapoints"][0]['Maximum']

	if cloudwatch_count["Datapoints"]:
		bucket_count = cloudwatch_count["Datapoints"][0]['Maximum']

	print('{0} \t\t {1} \t {2} \t {3}'.format(bucket.name, bucket.creation_date, bucket_size, bucket_count))
