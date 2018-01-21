import logging
import os.path
from urllib.parse import urlparse

import boto
from boto.exception import S3ResponseError


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
