# USAspending Flattened

## Overview

Load a denormalized, flattened view of USAspending data to MongoDB.

## Background

The [USAspending API](https://api.usaspending.gov/) serves data about U.S. federal spending. This API is one outcome of the [DATA Act](http://fedspendingtransparency.github.io/), the first U.S. open data law, which mandates that federal agencies report standardized spending information to the U.S. Department of the Treasury for subsequent publication.

The API is useful but not appropriate for bulk data downloads and analysis. Although Treasury has a good website ([beta.usaspending.gov](https://beta.usaspending.gov)) built on the API, the download capabilities are somewhat limited at this time.

One additional option for bulk access of the data is the PosgreSQL database that powers the API, which is [available via Amazon RDS snapshot](https://aws.amazon.com/public-datasets/usaspending/).

This project ingests the USAspending relational data, denormalizes it into a series of nested json objects, and loads it to MongoDB.

### Why?

For now, this is a mostly academic exercise to get some data pipeline, MongoDB, and AWS practice. Who knows, maybe it will turn out to be useful!

### Caveats

For the usual reasons of why APIs exist in the first place, bypassing the API and pulling this information directly from the underlying database isn't a great idea.

I worked on the DATA Act implementation team, know the data pretty well, and feel comfortable grabbing it from the database. That said, as time marches on, I'll know the data less well, and this code will become less reliable.


## Setup Instructions

### Prerequisites:

* Python 3
* PostgreSQL 9.6
* MongoDB 3.4.9 or greater


### Install

1. From the command line, clone the project repository to your preferred location: `git@github.com:bsweger/usaspending-export.git`
2. Change to the project directory: `cd usaspending-export`
3. Install Python dependencies: `pip install -r requirements.txt`
4. Create `config/config.ini` and fill in your config values accordingly (use `config/config_example` as a template)

### Loading Data

Coming soon!
