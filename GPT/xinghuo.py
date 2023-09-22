# encoding=utf-8
# created @2023/8/7
# created by zhanzq
#

import requests
import json


def xinghuo(query):
    url = "https://api.listenai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 11e701f1-1fb6-4820-a406-bbc35a6ea94e"
    }
    method = "POST"
    data = {'temperature': 0.85, 'max_tokens': 1024, 'messages': [{'role': 'user', 'content': query}]}
    payload = json.dumps(data)

    try:
        response = requests.request(method, url, headers=headers, data=payload)
        resp_obj = json.loads(response.text)
        resp = resp_obj.get("choices", [{}])[0].get("message", {}).get("content")
        return resp
    except Exception as e:
        print(e)
        return None


def multi_intent_api(query):
    url = "https://api.listenai.com/v1/makes"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 11e701f1-1fb6-4820-a406-bbc35a6ea94e"
    }
    method = "POST"
    payload = {
        "model": "spark-interface-1.0",
        "task": "intent_split",
        "messages": [
            {"role": "user", "content": query}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        resp_obj = json.loads(response.text)
        resp = resp_obj.get("choices")
        intent_lst = [it.get("intent") for it in resp]
        return intent_lst

    except Exception as e:
        print(e)
        return None
