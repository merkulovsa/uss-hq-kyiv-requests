import json
from notion_requests import create_page

def send_to_notion(database_id, item, amount, contact):
    data = {
        "properties": {
            "Назва потреби": {
                "title": [
                    {
                        "text": {
                            "content": f'{str(item)} ({str(contact)})'
                        }
                    }
                ]
            },
            "Необхідно": {
                "number": int(amount)
            },
            "Статус": {
                "select": {
                    "id": "2d826b77-7a7a-4896-8acf-704aab5ab6b5"
                }
            }
        },
        "icon": {
            "type": "emoji",
            "emoji": "💉"
        }
    }

    print(json.dumps(data, indent=4, sort_keys=True))
    #create_page(database_id, data)