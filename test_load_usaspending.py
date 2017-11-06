from mongomock import MongoClient
import pytest

from load_usaspending import load_awards, load_tas


@pytest.fixture
def tas_objects():
    test_tas = [
        '{"label": "001X0137", "ata": null, "aid": "001", "bpoa": null}',
        '{"label": "0862013/20140337", "ata": null, "aid": "086"}',
        '{"label": "012-0122007/20100181", "ata": "012", "aid": "016"}',
        '{"label": "0122012/20133542", "ata": null, "aid": "012"}'
    ]
    return test_tas


@pytest.fixture
def awards_objects():
    test_awards = [
        '{"piid": "ABC123", "type": "B"}',
        '''{
            "fain": "R01HD080292", "type": "04",
            "awarding_agency": {
                "cgac": "075", "name": "Department of Health & Human Services",
                "subtier_code": "7529",
                "subtier_name": "National Institutes of Health"},
            "recipient": {
                "unique_identifier": "038633251", "name": "Univer. of Buffalo",
                "business_types": "H",
                "business_categories": [
                    "public_institution_of_higher_ed", "higher_education"]},
            "recipient_location": {
                "state_abbr": "NY", "state": "NEW YORK", "city": "BUFFALO",
                "zip": "14260"},
            "accounting": [{
                "obligated_amount": 565496.00,
                "tas": {
                    "label": "07520170844", "aid": "075",
                    "main_account": "0844", "sub_account": "000",
                    "federal_account": {
                        "main_account_code": "0844"}},
                "object_class": {
                    "major_object_class_code": "4", "object_class_code": "41"},
                "program_activity": {
                    "program_activity_code": "1234"}
                }, {
                "obligated_amount": 62833.00,
                "tas": {
                    "label": "07520170844",
                    "federal_account": {"agency_identifier": "075"}
                    },
                    "object_class": {
                        "major_object_class_code": "40",
                        "object_class_code": "410"},
                "program_activity": {
                    "program_activity_code": "7890"}
                }
            ]}'''
    ]
    return test_awards


def test_load_tas(tas_objects):
    """Test inserting TAS documents."""
    collection = MongoClient().db.collection

    load_tas(collection, tas_objects)
    assert collection.count() == 4
    assert collection.find_one({'label': '001X0137'})


def test_load_awards(awards_objects):
    """Test inserting awards documents."""
    collection = MongoClient().db.collection

    load_awards(collection, awards_objects)
    assert collection.count() == 2
    assert collection.find_one({'accounting.tas.label': '07520170844'})
