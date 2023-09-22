# encoding=utf-8
# created @2023/9/22
# created by zhanzq
#

# 引用llm api
from xinghuo import xinghuo
from chatgpt import chatgpt, chatgpt_org
from chatglm import chat_glm


import json

from common_utils.text_io.excel import save_json_list_into_xlsx, load_json_list_from_xlsx
from common_utils.text_io.txt import load_from_json


def context_understanding(query, llm_api):
    prompt_left = """
你是AI助手，当我发送一个query（含有“上下文”和“当前输入”）时，你需要根据上下文信息对当前输入进行改写，使其具备完整的语义信息，并返回json格式数据。json结构必须是这样的：
{
    "context": "原始的上下文信息",
    "query": "根据上下文改写后的句子"
}
比如query=“上下文：打开空调。当前输入：向上吹风”，你要返回如下json：
{"context": "打开空调", "query":"空调设为向上吹风"}

query=“上下文：帮我打开热水器。当前输入：不需要了”，你要返回如下json：
{"context": "帮我打开热水器", "query":"不需要打开热水器了"}

现在query=“"""

    prompt_right = "”,你应该返回什么?请返回相应的json格式，不要任何多余的解释。"

    query = prompt_left + query + prompt_right
    resp = llm_api(query)

    return resp


def context_test(data_path, output_path, sheet_name, llm_api):
    data_lst = load_json_list_from_xlsx(xlsx_path=data_path, sheet_names=["上下文测试用例"])["上下文测试用例"]
    out_lst = []
    for item in data_lst:
        idx = item.get("用例id")
        context = item.get("第一句")
        curr_query = item.get("第二句")
        query = f"上下文：{context}。当前输入：{curr_query}"
        print(f"\n\ncase {idx}: {query}")
        resp = context_understanding(query, llm_api=llm_api)
        resp = resp.strip()
        try:
            resp = json.dumps(json.loads(resp), indent=4, ensure_ascii=False)
        except Exception as e:
            print(e)

        print(resp)
        out_lst.append({"case_id": idx, "query": query, "上下文改写": resp})

    save_json_list_into_xlsx(xlsx_path=output_path, sheet_name=sheet_name, json_lst=out_lst)
    return


def multi_intent_split(query, llm_api):
    resp = llm_api(query)
    return resp


def multi_intent_test(data_path, output_path, sheet_name, llm_api):
    data_lst = load_json_list_from_xlsx(xlsx_path=data_path, sheet_names=["多意图测试用例"])["多意图测试用例"]
    out_lst = []
    for item in data_lst:
        idx = item.get("用例id")
        query = item.get("用例名称")
        print(f"\n\ncase {idx}: {query}")
        resp = multi_intent_split(query, llm_api=llm_api)
        resp = resp.strip()
        try:
            resp = json.dumps(json.loads(resp), indent=4, ensure_ascii=False)
        except Exception as e:
            print(e)

        print(resp)
        out_lst.append({"case_id": idx, "query": query, "多意图信息": resp})

    save_json_list_into_xlsx(xlsx_path=output_path, sheet_name=sheet_name, json_lst=out_lst)
    return


def do_context_test():
    data_path = "/Users/zhanzq/Downloads/大模型测试.xlsx"
    output_path = "/Users/zhanzq/Downloads/llm_test.xlsx"

    sheet_name = "上下文理解-讯飞-0922"
    context_test(data_path, output_path=output_path, sheet_name=sheet_name, llm_api=xinghuo)

    sheet_name = "上下文理解-chatGPT-0922"
    context_test(data_path, output_path=output_path, sheet_name=sheet_name, llm_api=chatgpt)

    sheet_name = "上下文理解-chatGLM-0922"
    context_test(data_path, output_path=output_path, sheet_name=sheet_name, llm_api=chat_glm)

    return


def do_multi_intent_test():
    data_path = "/Users/zhanzq/Downloads/大模型测试.xlsx"
    output_path = "/Users/zhanzq/Downloads/llm_test.xlsx"

    sheet_name = "多意图拆解-讯飞-0922"
    multi_intent_test(data_path, output_path=output_path, sheet_name=sheet_name, llm_api=xinghuo)

    sheet_name = "多意图拆解-chatGPT-0922"
    multi_intent_test(data_path, output_path=output_path, sheet_name=sheet_name, llm_api=chatgpt)

    sheet_name = "多意图拆解-chatGLM-0922"
    multi_intent_test(data_path, output_path=output_path, sheet_name=sheet_name, llm_api=chat_glm)

    return


def main():
    resp = chatgpt_org("hello")
    print(resp)
    # # 加载prompt数据
    # prompt_path = "./prompt.json"
    # prompt_dct = load_from_json(json_path=prompt_path)
    # prompt = prompt_dct["multi_intent_prompt"]
    #
    # # 构造llm输入数据
    # query = "上下左右摆风"
    # query = prompt.replace("USER_INPUT", query)
    #
    # res = multi_intent_split(query=query, llm_api=chatgpt)
    # print(res)

    # context = "灯调暗一点"
    # curr_query = "还是太刺眼了"
    # query = f"上下文：{context}。当前输入：{curr_query}"
    # res = context_understanding(query=query, llm_api=xinghuo)
    # print(res)


if __name__ == "__main__":
    main()
