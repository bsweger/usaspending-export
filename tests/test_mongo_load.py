from mongomock import MongoClient
import pytest

from usaspending_export.mongo_load import load_documents


@pytest.fixture
def documents(tmpdir):
    data = (
        """{"label": "001X0137", "ata": null, "aid": "001", "bpoa": null}
        {"label": "0862013/20140337", "ata": null, "aid": "086"}
        {"label": "012-0122007/20100181", "ata": "012", "aid": "016"}
        {"label": "0122012/20133542", "ata": null, "aid": "012"}"""
        )

    test_file = tmpdir.mkdir("test_data").join("documents.json")
    test_file.write(data)
    return str(test_file)


def test_load_documents(documents):
    """Test inserting a series of JSON objects."""
    collection = MongoClient().db.collection
    collection.insert_one({"fain": "existingfain"})
    load_documents(collection, documents)

    # collection's existing data should be dropped before adding new documents
    assert collection.count() == 4
    assert collection.find_one({'label': '001X0137'})
    assert collection.find_one({'fain': 'existingfain'}) is None


@pytest.mark.skip(reason="need to mock/patch/refactor the s3 connection code")
def test_get_s3_key():
    pass
