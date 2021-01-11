import json
from chalicelib.alexa_list import ListEvent, AlexaList

EXAMPLE_EVENT = json.loads("""
{
    "version": "1.0",
    "context": {
        "System": {
            "application": {
                "applicationId": "AAAA"
            },
            "user": {
                "userId": "XXXX",
                "permissions": {
                    "consentToken": "YYYY"
                }
            },
            "apiEndpoint": "https://api.eu.amazonalexa.com",
            "apiAccessToken": "ZZZZ"
        }
    },
    "request": {
        "type": "AlexaHouseholdListEvent.ItemsCreated",
        "requestId": "d3dc26b2-660d-4acd-930a-277c2282941f",
        "timestamp": "2020-05-03T16:59:13Z",
        "eventCreationTime": "2020-05-03T16:59:13Z",
        "eventPublishingTime": "2020-05-03T16:59:13Z",
        "body": {
            "listId": "BBBB",
            "listItemIds": [
                "CCCC"
            ]
        }
    }
}
""")


def test_create_event():
    le = ListEvent(EXAMPLE_EVENT)

    assert le.type == "AlexaHouseholdListEvent.ItemsCreated"


def test_event_is_item_created_type():
    le = ListEvent(EXAMPLE_EVENT)

    assert le.is_item_created is True


def test_alexa_get_items_from_event(requests_mock):
    al = AlexaList()
    requests_mock.get('https://api.eu.amazonalexa.com/v2/householdlists/BBBB/items/CCCC', json={"item": "apple"})
    items = al.get_items_from_event(ListEvent(EXAMPLE_EVENT))

    assert items[0] == {"item": "apple"}
