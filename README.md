[![CircleCI](https://circleci.com/gh/bsweger/usaspending-export.svg?style=svg)](https://circleci.com/gh/bsweger/usaspending-export)
[![Maintainability](https://api.codeclimate.com/v1/badges/860f4b9e4a16c9645509/maintainability)](https://codeclimate.com/github/bsweger/usaspending-export/maintainability)
[![Test  Coverage](https://api.codeclimate.com/v1/badges/860f4b9e4a16c9645509/test_coverage)](https://codeclimate.com/github/bsweger/usaspending-export/test_coverage)

# USAspending Export

## Overview

Load a denormalized, flattened view of USAspending data to MongoDB.

## Background

The [USAspending API](https://api.usaspending.gov/) serves data about U.S. federal spending. This API is one outcome of the [DATA Act](http://fedspendingtransparency.github.io/), the first U.S. open data law, which mandates that federal agencies report standardized spending information to the U.S. Department of the Treasury for subsequent publication.

The API is useful but not appropriate for bulk data downloads and analysis. Treasury has a good website with download capability ([beta.usaspending.gov](https://beta.usaspending.gov)) built on the API, but I was after the data in a very specific, flattened format.

Luckily, the USAspending team provides a snapshot of their backend PostgreSQL database via [AWS Public Datasets](https://aws.amazon.com/public-datasets/usaspending/).

This project:

1. Ingests the USAspending relational data
2. Denormalizes it into a series of nested json objects and sends them to S3
3. Loads the denormalized data to MongoDB
4. Pulls data from MongoDB to .csv

**The MongoDB step is unecessary. Honestly, it's just there because I was learning mongo for an upcoming job.**


### Caveats

For the usual reasons of why APIs exist in the first place, bypassing the API and pulling this information directly from the underlying database isn't a great idea.

I worked on the DATA Act implementation team, know the data pretty well, and feel comfortable grabbing it from the database. That said, as time marches on, I'll know the data less well, and this code will become less reliable.


## Setup Instructions

### Prerequisites:

* Python 3.6 or higher
* PostgreSQL 9.6
* MongoDB 3.4.9 or greater
* An AWS account that can read and create S3 objects and can create and delete RDS instances.


### Install

1. From the command line, clone the project repository to your preferred location: `git@github.com:bsweger/usaspending-export.git`
2. Change to the project directory: `cd usaspending-export`
3. Install Python dependencies: `pip install -r requirements.txt`
4. Create `config/config.ini` and fill in your config values accordingly (use `config/config_example` as a template)

### Setup AWS Credentials

To restore the latest USAspending Postgres DB from the AWS public RDS snapshot and export its data to S3, you'll need to [configure AWS credentials for use by boto3](http://boto3.readthedocs.io/en/latest/guide/configuration.html). In addition to providing your access and secret access keys, set the default AWS region to `us-east-1` (the location of the public snapshot).

### Loading Data

**TODO:** Streamline all of this when there's a better idea of which pieces are actually useful and worthy of further tweaking.

1. Restore an RDS instance from the AWS public datasets snapshot
2. Verify db connectivity. If this doesn't work, check the security group settings of the RDS instance. It's likely that you need to allow inbound traffic on port 5432 (for postgres access).
3. Run queries that create the .json output.
4. Upload the .json output to an S3 get_bucket (make sure the names match the names specified in `config.ini`).
5. Load data to mongodb (**important:** prior data in the mongo collections is dropped before the new data is loaded). From the `usaspending_export` folder, run `python load_usaspending.py`.
6. Export a flattened version of the awards data to a .csv (will be named `usaspending_awards.csv`). From the `usaspending_export` folder, run `python flatten_usaspending.py`.
