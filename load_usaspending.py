import json
import logging
import os.path
from urllib.parse import urlparse

import boto
from boto.exception import S3ResponseError
from pymongo import MongoClient
import smart_open

from config.settings import settings


def load_usaspending():
    """Load usaspending info to mongodb."""
    # TODO: more robust logging setup and execution
    logging.basicConfig(level=logging.INFO)

    db = get_mongo_client()

    # For now, working under assumption that json data is somewhere on S3
    key = get_s3_key(settings['s3']['tas'])
    load_documents(db.tas, key)
    key = get_s3_key(settings['s3']['awards'])
    load_documents(db.awards, key)


def load_documents(collection, thefile):
    """Load a file of json objects to the specified mongodb collection."""
    with smart_open.smart_open(thefile) as data:
        count = 0
        for row in data:
            collection.insert_one(json.loads(row)).inserted_id
            count += 1
        logging.info(
            'Inserted {} documents into {}'.format(count, collection))


def get_mongo_client():
    """Return a mongo database."""
    mongo = settings['mongodb']

    client = MongoClient(mongo['host'], int(mongo['port']))
    db = client.usaspending
    return db


def get_s3_key(s3url):
    """Returns S3 key from URL."""
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


if __name__ == '__main__':
    load_usaspending()
