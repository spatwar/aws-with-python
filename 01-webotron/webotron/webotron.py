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
from domain import DomainManager

session = boto3.Session(profile_name='pythonAutomation')
bucket_manager = BucketManager(session)_9880372aa2354929e138ee53cf662b58.tljzshvwok.acm-validations.aws.
domain_manager = DomainManager(session)
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
def setup_bucket(bucket):
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


@cli.command('setup-domain')
@click.argument('domain')
@click.argument('bucket')
def setup_domain(domain, bucket):
  zone = domain_manager.find_hosted_zone(domain) \
       or domain_manager.create_hosted_zone(domain)
  print(zone)
  try:
      a_record = domain_manager.create_s3_domain_record(zone, domain)
  except ClientError as e:
      print(e.response['Error']['Code'] )


  print("Domain configure: http://{}".format(domain))
  print(a_record)


if __name__ == '__main__':
    cli()
