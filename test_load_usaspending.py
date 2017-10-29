from mongomock import MongoClient
import pytest

from load_usaspending import load_tas


@pytest.fixture
def tas_objects():
    test_tas = [
        '{"label" : "001X0137", "ata" : null, "aid" : "001", "bpoa" : null}',
        '{"label" : "0862013/20140337", "ata" : null, "aid" : "086"}',
        '{"label" : "012-0122007/20100181", "ata" : "012", "aid" : "016"}',
        '{"label" : "0122012/20133542", "ata" : null, "aid" : "012"}'
    ]
    return test_tas


def test_load_tas(tas_objects):
    """Test inserting TAS documents."""
    collection = MongoClient().db.collection

    load_tas(collection, tas_objects)
    assert collection.count() == 4
    assert collection.find_one({'label': '001X0137'})
