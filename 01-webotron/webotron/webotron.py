#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Webotron: Deploying Static websites to aws.

Webotron automates the process of deploying Static websites to aws
- Configure AWS S3 buckets
- Create then
- Set them for local website hosting
- Configure DNS with AWS Route 53
- Configure coding
"""

import boto3
import click


from bucket import BucketManager

session = boto3.Session(profile_name='pythonAutomation')
bucket_manager = BucketManager(session)
#s3 = session.resource('s3')


@click.group()
def cli():
    """Webotron deploys websites to AWS."""
    pass


@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets"""
    for bucket in bucket_manager.s3.buckets.all():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    for obj in bucket_manager.all_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket():
    new_bucket = bucket_manager.init_bucket(bucket)
    new_bucket.upload_file('/code/aws-with-python/01-webotron/index.html','index.html', ExtraArgs={'ContentType':'text/html'})
    bucket_manager.set_policy(new_bucket)
    bucket_manager.configure_website(new_bucket)


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    "Sync contents of the PATHNAME to Bucket"
    bucket_manager.sync(pathname, bucket)
    

if __name__ == '__main__':
    cli()
