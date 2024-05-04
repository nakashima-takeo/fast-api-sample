import json

import requests


def main():
    url = "http://127.0.0.1:8000/item/"
    body = {"name": "take", "description": "taketake", "price": 510, "tax": 0.1}
    res = requests.post(url, json.dumps(body))
    print(res.json())


if __name__ == "__main__":
    main()
