from lxml import etree
import requests
import re
from threading import Thread, Lock
import urllib.request


class Get_magnet:
    def get_html_str(self, url, refers=None):
        # 传入refer参数
        if refers:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
                'Referer': refers
            }
        else:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
            }
        response = requests.get(url, headers=header)
        html_str = response.content.decode()
        return html_str

    # def get_html_str(self, url, refers=None):
    #     # 传入refer参数
    #     rq=urllib.request.Request(url)
    #     if refers:
    #         rq.add_header('Referer', refers)
    #     rq.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36')
    #
    #
    #     response = urllib.request.urlopen(rq,timeout=30)
    #     html_str = response.read().decode()
    #     return html_str
    def parse_each_game(self, html_str):
        # 从游戏的连接返回游戏数据页的数据
        elements = etree.HTML(html_str)
        game_links = elements.xpath("//ul[@class='lcp_catlist']/li/a/@href")
        name = elements.xpath("//ul[@class='lcp_catlist']/li/a/@title")
        # 返回连接的
        return game_links

    def parse_magnet(self, html_str):
        # 获取magnet数据
        elements = etree.HTML(html_str)
        data = elements.xpath("//ul/li/a/@href")
        magnet = None
        name = None
        for each_data in data:
            magnet = re.match('magnet:\?xt=urn:btih:[\d|a-z|A-Z]+$', each_data)
            if magnet:
                # 获取到磁力再获取游戏名
                magnet = magnet.group()
                name = elements.xpath("//h1[@class='entry-title']/text()")[0]
                break
        return magnet, name

    def multithread(self, each_game, each_page):
        html_str = self.get_html_str(each_game, each_page)  # 传入游戏链家所在页url作为refers
        # 4.1获取游戏的magnet数据
        magnet, name = self.parse_magnet(html_str)
        if magnet:
            with open('game.txt', 'a+') as f:
                f.write(name + ':\n' + magnet + '\n\n')
            mutex.acquire()
            global num_success
            num_success += 1
            mutex.release()
            print(name)

    def run(self):
        # 主逻辑
        # 1生成地址

        links = []
        for i in range(1, 23):
            url = 'http://fitgirl-repacks.site/all-my-repacks-a-z/?lcp_page0={}#lcp_instance_0'.format(i)
            links.append(url)
        # 2获取当前页地址的数据
        for each_page in links:
            print(each_page + ':')
            html_str = self.get_html_str(each_page)
            # 3从数据中获取每个游戏的连接
            game_list = self.parse_each_game(html_str)
            threads = []
            for each_game in game_list:
                t1 = Thread(target=self.multithread, args=(each_game, each_page))
                threads.append(t1)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            print('saved %d games' % num_success)

        # 4循环获取每个游戏的数据

        # 4.3保存游戏数据
        # 5获取下一页，循环


def main():
    download = Get_magnet()
    download.run()


if __name__ == '__main__':
    num_success = 0
    mutex = Lock()
    main()
