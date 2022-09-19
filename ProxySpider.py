from requests import get


class ProxySpider:
    ip_list = list()

    def __init__(self, ip_number, proxypool_url):
        """

        :param ip_number:一次性获取的代理ip数
        :param proxypool_url: 获取代理的目标地址（http://192.168.99.100:5555/random）（http://127.0.0.1:5555/random）
        """
        self.proxypool_url = proxypool_url
        self.ip_number = ip_number

    def geturl(self):
        pass

    def parseurl(self):
        """
        向获取ip代理目标地址发送请求，返回代理
        :return:
        """
        for i in range(0, self.ip_number):
            if get(self.proxypool_url).status_code == 200:
                ProxySpider.ip_list.append(get(self.proxypool_url).text.strip())

            else:
                while get(self.proxypool_url).status_code == 200:
                    ProxySpider.ip_list.append(get(self.proxypool_url).text.strip())

    def run(self):
        """# 先清空已存的ip列表
        ProxySpider.ip_list = list()"""
        # 再获取新的ip列表
        self.parseurl()
