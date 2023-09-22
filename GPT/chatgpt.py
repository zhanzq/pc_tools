# encoding=utf-8
# created @2023/8/7
# created by zhanzq
#

import json
from hashlib import sha256
from urllib.parse import urlparse
import requests
import time


def remove_special_char(s, special_chars):
    if s is None or s.strip() == "":
        return ""
    s = s.strip()
    for ch in special_chars:
        s = s.replace(ch, "")

    return s


def get_signature(app_or_sys_id: str, app_or_sys_key: str, timestamp_ms, body: str, url: str):
    url_obj = urlparse(url)
    path = url_obj.path
    app_or_sys_key = remove_special_char(app_or_sys_key, '"')
    try:
        if type(body) is not str:
            body = json.dumps(body, ensure_ascii=False)
    except:
        body = ""
    body = remove_special_char(body, " \t\r\n")

    encrypt_str = path + body + app_or_sys_id + app_or_sys_key + timestamp_ms
    md5 = sha256()
    md5.update(encrypt_str.encode("utf8"))
    signature = md5.hexdigest()

    #     print(f"encrypt_str: {encrypt_str}")
    #     print(f"signature: {signature}")

    return signature


def content_check(content, system_id, system_key):
    url = "https://openservice.haigeek.com/restapi/technology/arch/cs/v1.0/textscan"
    body = {"content": content}
    timestamp = "{:.0f}".format(time.time() * 1000)
    sign = get_signature(system_id, system_key, timestamp, body, url)
    headers = {
        "systemId": system_id,
        "sign": sign,
        "timestamp": timestamp
    }

    resp = requests.post(url=url, headers=headers, json=body)
    resp_obj = json.loads(resp.content)

    return resp_obj


def chatgpt(query, system_id="SV-ISP99104971161-0000", system_key="c98da2bc5fd003b8198085e534d0875a", sys_prompt=""):
    url = "https://openservice.haigeek.com/restapi/jcjg/arch/llm/v1.0/chat/completions"
    body = {
        "messages": [
            {
                "role": "system",
                "content": sys_prompt
            },
            {
                "role": "user",
                "content": query
            }
        ]
    }

    timestamp = "{:.0f}".format(time.time() * 1000)
    sign = get_signature(system_id, system_key, timestamp, body, url)
    headers = {
        "systemId": system_id,
        "sign": sign,
        "timestamp": timestamp
    }
    try:
        resp = requests.post(url=url, headers=headers, data=json.dumps(body, ensure_ascii=False).encode("utf8"))
        resp_obj = json.loads(resp.content)

        return resp_obj["content"]["choices"][0]["message"]["content"]
    except Exception as e:
        print(e)
        return ""


def chatgpt_org(query):
    url = "https://api.openai.com/v1/chat/completions"

    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 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'
    }

    proxies = {
        "http": "http://127.0.0.1:1087",
        "https": "http://127.0.0.1:1087"
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
        resp_obj = json.loads(response.text)
        resp = resp_obj.get("choices", [{}])[0].get("message", {}).get("content")
        return resp
    except Exception as e:
        print(e)
        return None
