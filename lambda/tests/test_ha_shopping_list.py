from chalicelib.ha_shopping_list import HAShoppingList


TEST_HA_SHOPPING_LIST = '''
    [
        {"complete": false, "id": "4af1f40af18e457b80999a846239c02c", "name": "Queso Philadelphia"},
        {"complete": false, "id": "f427757e5bcf4e59af3edb4e11dc5b8f", "name": "Puerro"},
        {"complete": false, "id": "340fed61fdf14d618b678a78c0f86d7f", "name": "Alcachofas"},
        {"complete": false, "id": "4c712fd6671f4988b73c2a60a0265a3c", "name": "Pepinillos"}
    ]
'''


def test_ha_get_items(requests_mock):
    al = HAShoppingList('mock://aaaa.com', 'bbbb')
    requests_mock.get(
        'mock://aaaa.com/api/shopping_list',
        text=TEST_HA_SHOPPING_LIST,
        request_headers={"Authorization": "Bearer bbbb"})
    items = al.get_list()

    assert len(items) == 4
    assert list(items[0].keys()) == ["complete", "id", "name"]


def test_ha_get_items_names(requests_mock):
    al = HAShoppingList('mock://aaaa.com', 'bbbb')
    requests_mock.get(
        'mock://aaaa.com/api/shopping_list',
        text=TEST_HA_SHOPPING_LIST,
        request_headers={"Authorization": "Bearer bbbb"})
    items = al.get_list_names()

    assert len(items) == 4
    assert "queso philadelphia" in items


def test_add_items(requests_mock):
    al = HAShoppingList('mock://aaaa.com', 'bbbb')
    requests_mock.get(
        'mock://aaaa.com/api/shopping_list',
        text=TEST_HA_SHOPPING_LIST,
        request_headers={"Authorization": "Bearer bbbb"})
    requests_mock.post(
        'mock://aaaa.com/api/shopping_list/item',
        text='{"complete": false, "id": "61d090cc855a404abd8b1cc161a2da64", "name": "Manzanas"}',
        request_headers={"Authorization": "Bearer bbbb"})

    al.add('Manzanas')


def test_do_not_add_items_when_already_in_list(requests_mock):
    al = HAShoppingList('mock://aaaa.com', 'bbbb')
    requests_mock.get(
        'mock://aaaa.com/api/shopping_list',
        text=TEST_HA_SHOPPING_LIST,
        request_headers={"Authorization": "Bearer bbbb"})

    assert al.add('Puerro') is None

