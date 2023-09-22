# encoding=utf-8
# created @2023/8/7
# created by zhanzq
#

import requests
import json


def ernie(query):
    access_token = get_access_token()
    print(f"access_token: {access_token}")
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={access_token}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "messages": [
            {
                "role": "user",
                "name": None,
                "content": query,
            }
        ],
        "temperature": 0.95,
        # （1）较高的数值会使输出更加随机，而较低的数值会使其更加集中和确定
        # （2）默认0.95，范围 (0, 1.0]，不能为0
        # （3）建议该参数和top_p只设置1个
        # （4）建议top_p和temperature不要同时更改
        "top_p": 0.8,
        # （1）影响输出文本的多样性，取值越大，生成文本的多样性越强
        # （2）默认0.8，取值范围 [0, 1.0]
        # （3）建议该参数和temperature只设置1个
        # （4）建议top_p和temperature不要同时更改
        "penalty_score": 1.0,
        # 通过对已生成的token增加惩罚，减少重复生成的现象。说明：
        # （1）值越大表示惩罚越大
        # （2）默认1.0，取值范围：[1.0, 2.0]
        "stream": False,
        # 是否以流式接口的形式返回数据，默认false
        "user_id": None
        # 表示最终用户的唯一标识符，可以监视和检测滥用行为，防止接口恶意调用
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        resp_obj = json.loads(response.text)
        return resp_obj["result"]
    except Exception as e:
        print(e)
        return None


def get_access_token():
    with open("./config.json", "r") as reader:
        conf = json.load(reader)
    baidu_api_key = conf["baidu_api_key"]
    baidu_secret_key = conf["baidu_secret_key"]
    query_param = f"grant_type=client_credentials&client_id={baidu_api_key}&client_secret={baidu_secret_key}"
    url = "https://aip.baidubce.com/oauth/2.0/token?" + query_param

    try:
        resp = requests.post(url=url)
        resp_obj = json.loads(resp.text)

        return resp_obj["access_token"]
    except Exception as e:
        print(e)
        return None


def test():
    print(ernie("你好"))


def main():
    test()

    return


if __name__ == "__main__":
    main()
