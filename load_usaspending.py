import json
import logging
from urllib.parse import urlparse

from pymongo import MongoClient
from s3fs.core import S3FileSystem

from config.settings import settings


def load_usaspending():
    """Load usaspending info to mongodb."""
    # TODO: more robust logging setup and execution
    logging.basicConfig(level=logging.INFO)

    db = get_mongo_client()

    # For now, working under assumption that json data is somewhere on S3
    path = get_s3_path(settings['s3']['tas'])
    load_documents(db.tas, path)
    path = get_s3_path(settings['s3']['awards'])
    load_documents(db.awards, path)


def load_documents(collection, s3path):
    """Load a file of json objects to the specified mongod collection.

    Keyword arguments:
    collection -- mongo db collection to be loaded (existing data is dropped)
    s3path -- location of file w/ json objects to insert to mongo collection
    """
    count = collection.count()
    logging.info(
        'Dropped {} documents from {}'.format(count, collection.name)
    )
    collection.drop()

    s3 = S3FileSystem(anon=False)
    with s3.open(s3path, mode='rb') as data:
        count = 0
        for row in data:
            collection.insert_one(json.loads(row)).inserted_id
            count += 1
        logging.info(
            'Inserted {} documents into {}'.format(count, collection.name))


def get_mongo_client():
    """Return a mongo database."""
    mongo = settings['mongodb']

    client = MongoClient(mongo['host'], int(mongo['port']))
    db = client[mongo['dbname']]
    return db


def get_s3_path(s3url):
    """Return S3 key from URL."""
    s3 = S3FileSystem(anon=False)
    path = urlparse(s3url).path[1:]
    if not s3.exists(path):
        raise ValueError('Path not found on S3: {}'.format(path))
    return path


if __name__ == '__main__':
    load_usaspending()
