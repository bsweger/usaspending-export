import logging
import os.path
from urllib.parse import urlparse

import boto
from boto.exception import S3ResponseError
import boto3

logging.basicConfig(level=logging.INFO)
# make to boto-related loggers less verbose
logging.getLogger('boto').setLevel(logging.CRITICAL)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)


def get_s3_key(s3url):
    """Return S3 key from URL."""
    bucket, data = os.path.split(urlparse(s3url).path)
    # using boto instead of boto3 to avail ourselves of some
    # smart_open syntactic sugar when working with s3 data
    try:
        key = boto.connect_s3().get_bucket(bucket[1:]).get_key(data)
    except S3ResponseError:
        logging.error('Invalid S3 bucket: {}'.format(s3url))
        raise
    if key is None:
        raise ValueError('Object {} not found on S3: {}'.format(data, s3url))
    return key


def get_rds_info(arn):
    """Returns information about the USAspending public RDS snapshot."""
    logging.info(f'Getting RDS snapshot info {arn}')
    client = boto3.client('rds')
    response = client.describe_db_snapshots(
        DBSnapshotIdentifier=arn
    )
    return response


def restore_rds_snapshot(arn, instance_id='usaspending-restore'):
    """Restore the latest USAspending RDS snapshot from AWS public datasets."""
    # arn = 'arn:aws:rds:us-east-1:515495268755:snapshot:usaspending-db'
    logging.info(f'Starting restore of RDS snapshot {arn}')
    client = boto3.client('rds')
    response = client.restore_db_instance_from_db_snapshot(
        DBInstanceIdentifier=instance_id,
        DBSnapshotIdentifier=arn
    )

    # Don't return instance info until instance is available
    waiter = client.get_waiter('db_instance_available')
    waiter.wait(DBInstanceIdentifier=instance_id)
    response = client.describe_db_instances(DBInstanceIdentifier=instance_id)
    return response


def delete_rds_instance(instance_id):
    """Delete restored USASpending RDS instance."""
    logging.info(f'Deleting RDS instance {instance_id}')
    client = boto3.client('rds')
    response = client.delete_db_instance(
        DBInstanceIdentifier=instance_id,
        SkipFinalSnapshot=True
    )
    return response
