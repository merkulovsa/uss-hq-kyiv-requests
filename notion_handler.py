import requests, json

TOKEN = None
DATABASE_ID = None

with open('NOTION', 'r') as f:
    TOKEN, DATABASE_ID = [x.replace('\n', '') for x in f.readlines()]

HEADERS = {
    "Authorization": "Bearer " + TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}

def create_page(database_id, headers):
    create_url = 'https://api.notion.com/v1/pages'

    new_page_data = {
        "parent": { "database_id": database_id },
        "properties": {
            "Description": {
                "title": [
                    {
                        "text": {
                            "content": "Review"
                        }
                    }
                ]
            },
            "Value": {
                "rich_text": [
                    {
                        "text": {
                            "content": "Amazing"
                        }
                    }
                ]
            },
            "Status": {
                "rich_text": [
                    {
                        "text": {
                            "content": "Active"
                        }
                    }
                ]
            }
        }
    }
    
    data = json.dumps(new_page_data)
    res = requests.request("POST", create_url, headers=headers, data=data)

    print(res.status_code)
    print(res.text)

create_page(DATABASE_ID, HEADERS)