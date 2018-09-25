# -*- coding: utf-8 -*-

import uuid


"""Class for Route 53 domains."""

class DomainManager:


    """Manage a Route 53 domain."""
    def __init__(self, session):
        self.session = session
        self.client = self.session.client('route53')


    def find_hosted_zone(self, domain_name):
        paginator = self.client.get_paginator('list_hosted_zones')
        for page in paginator.paginate():
            for zone in page['HostedZones']:
                if domain_name.endswith(zone['Name'][:-1]):
                    return zone

        return None


    def create_hosted_zone(self , domain_name):
        zone_name = '.'.join(domain_name.split('.')[-2:])  # take the last 2 and remove the '.' at the end of xyz.abc.net. for ex
        print(zone_name)
        return self.client.create_hosted_zone(
            Name = zone_name,
            CallerReference = str(uuid.uuid4())

        )

    def create_s3_domain_record(self, zone, domain_name):
        return self.client.change_resource_record_sets(
            HostedZoneId = zone['Id'],
            ChangeBatch={
                'Comment': 'Created by Webotron',
                'Changes': [{
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': domain_name,
                            'Type': 'A',
                            'AliasTarget': {
                                'HostedZoneId': 'Z3AQBSTGFYJSTF',
                                'DNSName': 's3-website-us-east-1.amazonaws.com',
                                'EvaluateTargetHealth': False
                                },

                            }
                },
                ]
            }
        )
