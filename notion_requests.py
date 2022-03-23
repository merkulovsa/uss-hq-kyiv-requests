import requests, json
from time import time

__TOKEN = None

with open('INTEGRATION', 'r') as f:
    __TOKEN = f.read()

__HEADERS = {
    "Authorization": "Bearer " + __TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

def __read_request(database_id, start_cursor):
    payload = {}
    read_url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    if start_cursor is not None:
        payload['start_cursor'] = start_cursor

    res = requests.request("POST", read_url, json=payload, headers=__HEADERS)

    return res.json()

def read_database(database_id) -> str:
    data = __read_request(database_id, None)
    start_cursor = data['next_cursor']
    has_more = data['has_more']

    while has_more:
        _data = __read_request(database_id, start_cursor)

        data['results'] += _data['results']
        start_cursor = _data['next_cursor']
        has_more = _data['has_more']

    filename = './db-' + str(time()) + '.json'

    with open(filename, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)
        return filename

def update_page(page_id, update_data) -> str:
    update_url = f"https://api.notion.com/v1/pages/{page_id}"
    data = json.dumps(update_data)

    response = requests.request("PATCH", update_url, headers=__HEADERS, data=data)

    return response.status_code

def create_page(database_id, create_data) -> str:
    create_url = f"https://api.notion.com/v1/pages"

    create_data["parent"] = { "database_id": database_id }
    data = json.dumps(create_data)

    response = requests.request("POST", create_url, headers=__HEADERS, data=data)

    return response.status_code
