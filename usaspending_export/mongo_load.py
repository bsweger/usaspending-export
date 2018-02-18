import json
import logging

import smart_open

from util.settings import settings
from util.aws import get_s3_key
from util.mongo import get_mongo_client


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
    """Load a file of json objects to the specified mongod collection.

    Keyword arguments:
    collection -- mongo db collection to be loaded (existing data is dropped)
    thefile -- a file of json objects to insert to the mongo collection
    Load a file of json objects to the specified mongodb collection.
    """
    count = collection.count()
    logging.info(
        'Dropped {} documents from {}'.format(count, collection.name)
    )
    collection.drop()
    with smart_open.smart_open(thefile) as data:
        count = 0
        for row in data:
            collection.insert_one(json.loads(row)).inserted_id
            count += 1
        logging.info(
            'Inserted {} documents into {}'.format(count, collection.name))


if __name__ == '__main__':
    load_usaspending()
