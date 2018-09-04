#!/usr/bin/env python3.6

import boto3
import click
from botocore.exceptions import ClientError

session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')

@click.group()
def cli():
    "Webotron deploys websites to AWS"
    pass


@cli.command('list-buckets')
def list_buckets():
    "List all s3 buckets"
    for bucket in s3.buckets.all():
        print(bucket)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket():
    new_bucket = None
    try:
        new_bucket = s3.create_bucket(Bucket=bucket)
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            new_bucket = s3.Bucket(bucket)
        else:
            raise e


    new_bucket.upload_file('/code/aws-with-python/01-webotron/index.html','index.html', ExtraArgs={'ContentType':'text/html'})
    policy = """
    {
        "Version":"2012-10-17",
        "Statement":[{
        "Sid":"PublicReadGetObject",
        "Effect":"Allow",
        "Principal": "*",
            "Action":["s3:GetObject"],
            "Resource":["arn:aws:s3:::%s/*"
            ]
          }
        ]
    }
    """ % new_bucket.name
    policy = policy.strip()
    pol = new_bucket.Policy()
    pol.put(Policy=policy)
    ws = new_bucket.Website()
    ws.put( WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }})
    url = "https://%s.s3-website-us-east-1.amazonaws.com" % new_bucket.name



if __name__ == '__main__':
    cli()
