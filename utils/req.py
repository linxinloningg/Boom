# encoding=utf8
# 请求的方法
import os
from httpx import Limits, Client, AsyncClient, Response, HTTPError
from typing import Union, List
from asyncio import Semaphore, ensure_future, gather
from utils.models import API
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


def req_api(api: API, client: Union[Client, AsyncClient]) -> Response:
    """

    :param api:
    :param client:
    :return:
    """
    if isinstance(api.data, dict):
        resp = client.request(method=api.method, json=api.data,
                              headers=api.header, url=api.url, timeout=10)
    else:
        resp = client.request(method=api.method, data=api.data,
                              headers=api.header, url=api.url, timeout=10)
    return resp


def req_func_by_proxy(api: Union[API, str], phone: Union[tuple, str], proxy: dict) -> bool:
    """
    通过代理请求接口方法
    :param api:
    :param phone:
    :param proxy:
    :return:
    """
    # 多手机号支持
    if isinstance(phone, tuple):
        phone_lst = [_ for _ in phone]
    else:
        phone_lst = [phone]
    with Client(headers={'User-Agent': choice(headers)}, verify=False, proxies=proxy) as client:
        for ph in phone_lst:
            try:
                if isinstance(api, API):
                    api = api.handle_api(ph)
                    resp = req_api(api, client)
                    print("{}-{}".format(api.desc, resp.text[:30]))
                else:
                    api = api.replace("[phone]", ph).replace(" ", "").replace('\n', '').replace('\r', '')
                    resp = client.get(url=api, headers={'User-Agent': choice(headers)})
                    print("GETAPI接口-{}".format(resp.text[:30]))
                return True
            except HTTPError as e:
                print("请求失败{}".format(e))
                return False


def req_func(api: Union[API, str], phone: Union[tuple, str]) -> bool:
    """
    请求接口方法
    :param api:
    :param phone:
    :return:
    """
    # 多手机号支持
    if isinstance(phone, tuple):
        phone_lst = [_ for _ in phone]
    else:
        phone_lst = [phone]
    with Client(headers={'User-Agent': choice(headers)}, verify=False) as client:
        for ph in phone_lst:
            try:
                if isinstance(api, API):
                    api = api.handle_api(ph)
                    resp = req_api(api, client)
                    print("{}-{}".format(api.desc, resp.text[:30]))
                else:
                    api = api.replace("[phone]", ph).replace(" ", "").replace('\n', '').replace('\r', '')
                    resp = client.get(url=api, headers={'User-Agent': choice(headers)})
                    print("GETAPI接口-{}".format(resp.text[:30]))
                return True
            except HTTPError as e:
                print("请求失败{}".format(e))
                return False


async def run_async_by_proxy(apis: List[Union[API, str]], phone: Union[tuple, str], proxy: dict):
    """
    带有代理的异步请求
    :param apis:
    :param phone:
    :param proxy:
    :return:
    """
    async def async_reqs(src: Union[API, str]):
        """
        异步请求方法
        :param src:
        :return:
        """
        # 多手机号支持
        if isinstance(phone, tuple):
            phone_lst = [_ for _ in phone]
        else:
            phone_lst = [phone]
        async with semaphore:
            async with AsyncClient(
                    limits=Limits(max_connections=1000,
                                  max_keepalive_connections=2000),
                    headers={'User-Agent': choice(headers)},
                    proxies=proxy,
                    verify=False,
                    timeout=99999
            ) as c:

                for ph in phone_lst:
                    try:
                        if isinstance(src, API):
                            src = src.handle_api(ph)
                            r = await req_api(src, c)
                        else:
                            # 利用元组传参安全因为元组不可修改
                            s = (src.replace(" ", "").replace("\n", "").replace("\t", "").replace(
                                "&amp;", "").replace('\n', '').replace('\r', ''),)
                            r = await c.get(*s)
                        return r
                    except HTTPError as e:
                        print("异步请求失败{}".format(type(e)))
                    except TypeError:
                        print("类型错误")
                    except Exception as e:
                        print("异步失败{}".format(e))

    def callback(result):
        """异步回调函数"""
        log = result.result()
        if log is not None:
            print("请求结果:{}".format(log.text[:30]))

    tasks = []

    for api in apis:
        semaphore = Semaphore(999999)
        task = ensure_future(async_reqs(api))
        task.add_done_callback(callback)
        tasks.append(task)

    await gather(
        *tasks
    )


async def run_async(apis: List[Union[API, str]], phone: Union[tuple, str]):
    """
    异步请求
    :param apis:
    :param phone:
    :return:
    """
    async def async_reqs(src: Union[API, str]):
        """
        异步请求方法
        :param src:
        :return:
        """
        # 多手机号支持
        if isinstance(phone, tuple):
            phone_lst = [_ for _ in phone]
        else:
            phone_lst = [phone]
        async with semaphore:
            async with AsyncClient(
                    limits=Limits(max_connections=1000,
                                  max_keepalive_connections=2000),
                    headers={'User-Agent': choice(headers)},
                    verify=False,
                    timeout=99999
            ) as c:

                for ph in phone_lst:
                    try:
                        if isinstance(src, API):
                            src = src.handle_api(ph)
                            r = await req_api(src, c)
                        else:
                            # 利用元组传参安全因为元组不可修改
                            s = (src.replace(" ", "").replace("\n", "").replace("\t", "").replace(
                                "&amp;", "").replace('\n', '').replace('\r', ''),)
                            r = await c.get(*s)
                        return r
                    except HTTPError as e:
                        print("异步请求失败{}".format(type(e)))
                    except TypeError:
                        print("类型错误")
                    except Exception as e:
                        print("异步失败{}".format(e))

    def callback(result):
        """异步回调函数"""
        log = result.result()
        if log is not None:
            print("请求结果:{}".format(log.text[:30]))

    tasks = []

    for api in apis:
        semaphore = Semaphore(999999)
        task = ensure_future(async_reqs(api))
        task.add_done_callback(callback)
        tasks.append(task)

    await gather(
        *tasks
    )
