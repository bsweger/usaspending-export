import configparser
import json
import logging

from pymongo import MongoClient


def load_usaspending():
    """Load usaspending info to mongodb."""
    # TODO: more robust logging setup and execution
    logging.basicConfig(level=logging.INFO)

    db = get_mongo_client()

    # Insert Treasury Account Symbol (TAS) documents
    tas = db.tas
    with open('data/tas.json') as data:
        return load_tas(tas, data)


def load_tas(collection, file):
    """Load usaspending account data."""
    for row in file:
        obj = json.loads(row)
        tas_id = collection.insert_one(obj).inserted_id
        logging.info('Inserted TAS {} as {}'.format(obj.get('label'), tas_id))


def get_mongo_client():
    """Return a mongo database."""
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    mongo = config['mongodb']

    client = MongoClient(mongo['host'], int(mongo['port']))
    db = client.usaspending
    return db


if __name__ == '__main__':
    load_usaspending()
