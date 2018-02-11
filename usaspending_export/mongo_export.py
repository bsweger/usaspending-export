import logging
import subprocess

from util.mongo import get_mongo_client
from util.settings import settings


def pipeline_awards(collection):
    """Create a new collection of normalized awards."""
    # TODO: more robust logging setup and execution
    logging.basicConfig(level=logging.INFO)
    db = get_mongo_client()

    # define the mongo pipeline:
    # 1. $project: exclude _id from the pipeline to prevent duplicate errors
    #    on normalized data
    # 2. $unwind: create a separate document for each account on an award
    # 3. $out: the new collection to store the results
    pipeline = [
        {'$project': {'_id': 0}},
        {'$unwind': '$accounting'},
        {'$out': collection}
    ]

    # run the pipeline against the awards collection
    logging.info('Normalizing usaspending awards...')
    db.command(
        'aggregate', 'awards', pipeline=pipeline
    )


def export_awards(collection, file):
    """Export collection to .csv."""
    db = settings['mongodb']['dbname']

    args = ['mongoexport']
    args.append(f'-d={db}')
    args.append(f'-c={collection}')
    args.append('--fieldFile=fields_awards.txt')
    args.append('--type=csv')
    args.append(f'-o={file}')

    logging.info('Exporting normalized awards to csv...')
    subprocess.run(args)


if __name__ == '__main__':
    pipeline_awards('awards_flat')
    export_awards('awards_flat', 'usaspending_awards.csv')
