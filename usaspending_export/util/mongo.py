from pymongo import MongoClient

from .settings import settings


def get_mongo_client():
    """Return a mongo database."""
    mongo = settings['mongodb']

    client = MongoClient(mongo['host'], int(mongo['port']))
    db = client[mongo['dbname']]
    return db
