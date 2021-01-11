from os import getenv
from os.path import join
import logging

import requests
from chalice import Chalice

app = Chalice(app_name='shopping-list')
app.log.setLevel(logging.INFO)

HA_HOST = getenv('HA_HOST')
HA_TOKEN = getenv('HA_TOKEN')


class HAShoppingList:

    _ha_shopping_list_endpoint = 'api/shopping_list'

    def __init__(self, ha_host, token):
        self._token = token
        self.ha_post_url = join(ha_host, self._ha_shopping_list_endpoint, "item") if self._token else ha_host
        self._headers = {"Authorization": f"Bearer {self._token}"} if self._token else {}

    def add(self, item):
        item_dict = {'name': item}
        response = requests.post(self.ha_post_url, headers=self._headers, json=item_dict)
        app.log.info(str(response.status_code))


class ListEvent:

    def __init__(self, event):
        self.type = event['request']['type']
        self.body = event['request']['body']
        self.alexa_list = event['request']['body']['listId']
        self.alexa_items = event['request']['body']['listItemIds']
        self.user = event['context']['System']['user']
        self.api_endpoint = event['context']['System']['apiEndpoint']
        self.api_token = event['context']['System']['apiAccessToken']

    @property
    def is_item_created(self):
        return self.type == "AlexaHouseholdListEvent.ItemsCreated"

    @property
    def is_item_deleted(self):
        return self.type == "AlexaHouseholdListEvent.ListDeleted"


class ListItem:

    def __init__(self, **kwargs):
        self.created_time = kwargs['createdTime']
        self.id = kwargs['id']
        self.href = kwargs['href']
        self.status = kwargs['status']
        self.value = kwargs['value']


class AlexaList:

    def __init__(self, event=None, household_endpoint=None):
        self.household_endpoint = household_endpoint or 'v2/householdlists/'
        if event:
            a_list = self._get_list(event)
            self.list_id = a_list['listId']
            self.name = a_list['name']
            self.items = [ListItem(**item) for item in a_list['items']]

    @property
    def is_shopping_list(self):
        return self.name == "Alexa shopping list"

    def get_list_active_items_endpoint(self, api_endpoint, alexa_list=None):
        return join(api_endpoint, self.household_endpoint, alexa_list, "active")

    def get_item_endpoint(self, api_endpoint, alexa_list, item_id):
        return join(api_endpoint, self.household_endpoint, alexa_list, "items", item_id)

    def _get_list(self, event):
        url = self.get_list_active_items_endpoint(event.api_endpoint, event.alexa_list)
        headers = {
            'Content-Type': 'json',
            'Authorization': f'Bearer {event.api_token}'
        }
        response = requests.get(url=url, headers=headers)
        return response.json()

    def get_items_from_event(self, event):
        headers = {
            'Content-Type': 'json',
            'Authorization': f'Bearer {event.api_token}'
        }
        items_data = []
        for item in event.alexa_items:
            url = self.get_item_endpoint(event.api_endpoint, event.alexa_list, item)
            response = requests.get(url=url, headers=headers)
            items_data.append(response.json())
        return items_data



@app.lambda_function()
def lambda_handler(event, context):
    app.log.info(str(event))
    list_event = ListEvent(event)
    app.log.info(f"Event type is {list_event.type}")
    if not list_event.is_item_created:
        app.log.info(f"Nothing to do")
        return

    alexa_list = AlexaList(list_event)

    app.log.info(f"List name is {alexa_list.name}")
    if not alexa_list.is_shopping_list:
        app.log.info(f"Nothing to do")
        return

    items = alexa_list.get_items_from_event(list_event)

    ha_list = HAShoppingList(HA_HOST, HA_TOKEN)

    for item in items:
        app.log.info(f"Adding [{item['value']}] to HA")
        ha_list.add(item['value'].title())

