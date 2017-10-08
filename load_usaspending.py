import configparser
import logging

from pymongo import MongoClient


def load_usaspending():
    """Load usaspending info to mongodb."""
    # TODO: more robust logging setup and execution
    logging.basicConfig(level=logging.INFO)

    db = get_mongo_client()
    logging.info('Successfully connected to mongodb: {}'.format(db))


def get_mongo_client():
    """Return a mongo database."""
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    mongo = config['mongodb']
    # TODO: error checking for mongo config

    client = MongoClient(mongo['host'], int(mongo['port']))
    db = client.usaspending
    return db


if __name__ == '__main__':
    load_usaspending()
