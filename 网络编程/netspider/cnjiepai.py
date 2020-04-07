from urllib import request
from lxml import etree
import os
from threading import Thread, Semaphore,enumerate


def grt_html_str(url, refer=None):
    head = {
        'cookie': '__cfduid=dcdbb8756489b90242bc37d7f58684dfe1550717555',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36'
    }
    rq = request.Request(url, headers=head)
    if refer:
        rq.add_header('refer', refer)
    response = request.urlopen(rq)
    return response.read()


# url = 'https://www.cnjiepai.com/'
#
# html_str = grt_html_str(url).decode()
# elements = etree.HTML(html_str)
# links = elements.xpath("//div[@class='threadlist_title pull_left']/a/@href")
#
# for each_url in links:
#     html_str=grt_html_str(each_url,url)
#     pic_links=etree.HTML(html_str).xpath("//img/@data-src")
#     title=etree.HTML(html_str).xpath("//h1/text()")
#     print(title)
#     print(pic_links)


class Jiepai(object):

    def __init__(self, url):
        self.url = url
        self.sem = Semaphore(8)

    def get_html(self, url, refer=None):
        rq = request.Request(url)
        rq.add_header(
            'cookie', '__cfduid=dcdbb8756489b90242bc37d7f58684dfe1550717555'
        )
        rq.add_header(
            'user-agent',
                      'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36'
        )
        if refer:
            rq.add_header('refer', refer)
        try:
            response = request.urlopen(rq, timeout=10)
            html = response.read()
            return html
        except:
            print('%s timeout' % url)
            self.sem.release()
            exit(0)

    def parse_html(self, html_str, type):
        elements = etree.HTML(html_str)
        if type == 0:
            links = elements.xpath("//div[@class='threadlist_title pull_left']/a/@href")
            return links
        if type == 1:
            pic_links = elements.xpath("//img/@data-src")
            title = elements.xpath("//h1/text()")[0]
            return title, pic_links

    def save_pic(self, url, dir_name):
        filename = url.split('/')[-1]
        html = self.get_html(url)
        with open(dir_name + '/' + filename, 'wb') as f:
            f.write(html)

        print('%s success' % filename)
        self.sem.release()

    def run(self):
        # 多线程下载
        # 1获取网页url的数据
        html_str = self.get_html(self.url).decode()
        # 2分析数据获取每个帖子链接
        main_links = self.parse_html(html_str, 0)
        for each_lin in main_links:
            html_str = self.get_html(each_lin, self.url)
            # 3分析出图片链接
            title, pic_links = self.parse_html(html_str, 1)
            print(title)
            dir_name = 'D://小说/{}'.format(title)
            threads = []
            try:
                os.mkdir(dir_name)
                # os.chdir(dir_name)
            except:
                # os.chdir(dir_name)
                pass
            for each_pic in pic_links:
                t = Thread(target=self.save_pic, args=(each_pic, dir_name))
                threads.append(t)
            for t in threads:
                t.start()
                self.sem.acquire()
            for t in threads:
                t.join()
            os.chdir('..')


def main():
    obj = Jiepai('https://www.cnjiepai.com/tags/%E8%82%89%E4%B8%9D.html')
    obj.run()


if __name__ == '__main__':
    main()
