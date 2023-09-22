# encoding=utf-8
# created @2023/8/1
# created by zhanzq
#

import requests
import json


config_path = "./config.json"
config = json.load(open(config_path, "r", encoding="utf8"))
authorization = config.get("authorization")
cookie = config.get("cookie")
agent = config.get("agent")


def __get_context_id(query):
    url = "https://chatglm.cn/chatglm/backend-api/v1/stream_context"

    headers = {
        "authority": "chatglm.cn",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "authorization": authorization,
        "content-type": "application/json;charset=UTF-8",
        "cookie": cookie,
        "origin": "https://chatglm.cn",
        "referer": "https://chatglm.cn/detail",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": agent
    }
    method = "POST"
    data = {'prompt': query, 'seed': 63158, 'max_tokens': 512, 'conversation_task_id': '64b4b3ee93ee62246541ff1a',
            'retry': False, 'retry_history_task_id': None}

    payload = json.dumps(data)

    try:
        response = requests.request(method, url, headers=headers, data=payload)
        obj_resp = json.loads(response.text)

        context_id = obj_resp.get("result", {}).get("context_id")
        return context_id
    except Exception as e:
        print(e)
        return None


def __get_response(context_id):
    if not context_id:
        return None
    url = f"https://chatglm.cn/chatglm/backend-api/v1/stream?context_id={context_id}"

    headers = {
        "authority": "chatglm.cn",
        "accept": "text/event-stream",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "cookie": cookie,
        "referer": "https://chatglm.cn/detail",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": agent
    }
    method = "GET"
    payload = ""

    response = requests.request(method, url, headers=headers, data=payload)

    return response


def chat_glm(query):
    try:
        context_id = __get_context_id(query)
        response = __get_response(context_id)
        # print(response.text)
        resp = response.text.split("event:finish")[-1]
        resp = resp.strip().replace("data:", "")
        return resp
    except Exception as e:
        print(e)
        return None

