# -*- coding: utf-8 -*-

"""Class for S3 Bucket."""
from pathlib import Path
import mimetypes
from botocore.exceptions import ClientError

class BucketManager:
    """Manage an S3 Bucket."""


    def __init__(self, session):
        """Create a bucket Manager."""
        self.s3 = session.resource('s3')


    def all_buckets(self):
        """Get an iterator for all buckets."""
        return self.s3.buckets.all()


    def all_objects(self, bucket):
        """ Get an iterator for all objects in bucket."""
        return self.s3.Bucket(bucket).objects.all()


    def init_bucket(self, bucket_name):
        new_bucket = None
        try:
            new_bucket = self.s3.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                new_bucket = self.s3.Bucket(bucket)
            else:
                raise e
        return new_bucket


    def set_policy(self, bucket):
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
        """ % bucket.name
        policy = policy.strip()
        pol = bucket.Policy()
        pol.put(Policy=policy)

    def configure_website(self, bucket):
        ws = bucket.Website()
        ws.put( WebsiteConfiguration={
                'ErrorDocument': {
                    'Key': 'error.html'
                },
                'IndexDocument': {
                    'Suffix': 'index.html'
                }})
        url = "https://%s.s3-website-us-east-1.amazonaws.com" % bucket.name

    @staticmethod
    def upload_file(bucket, path , key):
        """Upload path to S3."""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'
        bucket.upload_file(
            path,
            key,
            ExtraArgs={
                'ContentType':'text/html'
            })

    def sync(self, pathname, bucket):
        new_bucket = self.s3.Bucket(bucket)
        root = Path(pathname).expanduser().resolve()
        def handle_directory(target):
            for p in target.iterdir():
                if p.is_dir(): handle_directory(p)
                if p.is_file(): self.upload_file(new_bucket, str(p) , str(p.relative_to(root)))

        handle_directory(root)
