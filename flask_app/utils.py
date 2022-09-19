# encoding=utf8
import os
from httpx import Client, Response
from .model import API
from random import choice

headers = list()
if os.path.exists("useragents"):
    txt_list = os.listdir("useragents")
    for txt in txt_list:
        try:
            with open("./useragents/{}".format(txt), 'r', encoding="UTF-8") as f:
                headers.extend(f.read().split('\n'))
        except Exception:
            continue


def test_resq(api: API, phone) -> Response:
    """测试 API 返回响应
    :param api: API model
    :param phone: 手机号
    :return: httpx 请求对象.
    """
    api = api.handle_API(phone)
    with Client(headers={'User-Agent': choice(headers)}, timeout=8) as client:
        # 这个判断没意义.....但是我不知道怎么优化...
        # https://stackoverflow.com/questions/26685248/difference-between-data-and-json-parameters-in-python-requests-package
        # Todo: json 和 data 表单发送的问题,有些服务器不能解释 json,只能接受表单
        # sol: 1. 添加额外字段判断...
        if not isinstance(api.data, dict):
            print("data")
            resp = client.request(method=api.method, headers=api.header,
                                  url=api.url, data=api.data)
        else:
            print('json')
            resp = client.request(
                method=api.method, headers=api.header, url=api.url, json=api.data)

    return resp


if __name__ == '__main__':
    pass
