# encoding=utf8
# 一些模型
import os
from pydantic import BaseModel
from typing import Union, Optional
from datetime import datetime
from json import loads
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


class API(BaseModel):
    """处理自定义 API 数据"""
    desc: str = "Default"
    url: str
    method: str = "GET"

    header: Optional[Union[str, dict]] = {'User-Agent': choice(headers)}

    data: Optional[Union[str, dict]]

    def replace_data(self, content: Union[str, dict], phone: str) -> str:
        """

        :param content:
        :param phone:
        :return:
        """
        # 统一转换成 str 再替换. ' -> "
        if phone:
            content = str(content).replace("[phone]", phone).replace(
                "[timestamp]", self.timestamp_new()).replace("'", '"')

        # 尝试 json 化
        try:
            return loads(content.replace("'", '"'))
        except:
            return content

    @staticmethod
    def timestamp_new() -> str:
        """
        返回整数字符串时间戳
        :return:
        """
        return str(int(datetime.now().timestamp()))

    def handle_api(self, phone: str = None):
        """
        传入手机号处理 API
        :param phone:
        :return:
        """

        # 仅仅当传入 phone 参数时添加 Referer
        # fix: 这段代码很有问题.......
        if phone:
            # 进入的 header 是个字符串
            if self.header == "":
                self.header = {'Referer': self.url}

        self.header = self.replace_data(self.header, phone)
        if not self.header.get('Referer'):
            self.header['Referer'] = self.url  # 增加 Referer

        self.data = self.replace_data(self.data, phone)
        self.url = self.replace_data(self.url, phone)
        # print(self)
        return self
