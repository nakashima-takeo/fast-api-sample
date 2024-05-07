"""Test API."""

import json

import requests


def main():
    """メイン関数です。

    この関数は、指定されたURLにPOSTリクエストを送信し、レスポンスを表示します。

    Args:
      None

    Returns:
      None
    """
    url = "http://127.0.0.1:8000/item/"
    body = {"name": "take", "description": "taketake", "price": 510, "tax": 0.1}
    res = requests.post(url, json.dumps(body), timeout=10)
    print(res.json())


if __name__ == "__main__":
    main()
