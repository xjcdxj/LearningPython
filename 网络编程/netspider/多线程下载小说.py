import gzip

from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import re
import os
from urllib import request
from fake_useragent import UserAgent
import pickle


class App():
    def __init__(self, url=None, code='utf-8', xpathOfNovelName=None, xpathOfChaptersUrl=None, xpathOfTitle=None,
                 xpathOfText=None):
        self.threadPool = ThreadPoolExecutor(10)
        self.ua = UserAgent()
        self.header = {}
        self.xpathOfNovelName = xpathOfNovelName
        self.xpathOfChaptersUrl = xpathOfChaptersUrl
        self.xpathOfTitle = xpathOfTitle
        self.xpathOfText = xpathOfText
        self.url = url
        self.code = code
        pass

    def gethtml(self, url):
        # self.header["User-Agent"] = self.ua.random
        rq = request.Request(url, headers=self.header)

        try:
            response = request.urlopen(rq, timeout=10)

            if response.getcode() == 200:
                return response
            else:
                print(response.getcode())
        except Exception as e:
            print('Failed %s' % e)

            return None

    def parseHtml(self, html='', requestCode=0):

        if requestCode == 0:  # 获取小说名字
            response = self.gethtml(self.url)
            if response:
                if 'Content-Encoding' in response.info() and response.info()['Content-Encoding'] == 'gzip':
                    print("gzip decompress")
                    html = gzip.decompress(response.read()).decode(self.code, errors="ignore")
                else:
                    html = response.read().decode(self.code, "ignore")
                element = etree.HTML(html)
                name = element.xpath(self.xpathOfNovelName)
                urls = element.xpath(self.xpathOfChaptersUrl)
                urls = sorted(list(set(urls)))
                chaptersUrl = {}
                count = 0
                for i in urls:
                    # chaptersUrl[count] = "http://biquto.com%s" % i
                    a = self.url.split('/')
                    b = i.split('/')
                    if len(a[-1]) == 0:
                        a = a[:-1]
                    if len(b[0]) == 0:
                        b = b[1:]
                    urlTemp = ''
                    for i in a:
                        if i != b[0]:
                            if i == "index.html":
                                break
                            urlTemp = urlTemp + i + '/'
                        else:
                            break
                    for c in range(len(b)):
                        urlTemp = urlTemp + b[c]
                        if c == len(b) - 1:
                            break
                        else:
                            urlTemp = urlTemp + '/'
                    chaptersUrl[count] = urlTemp

                    count += 1
                if name:
                    return name[0], chaptersUrl

                pass
        element = etree.HTML(html)
        if requestCode == 1:  # 获取章节链接

            # urls = element.xpath("//div[@id='list'][2]//dd/a/@href")
            urls = element.xpath(self.xpathOfChaptersUrl)
            urls = sorted(list(set(urls)))
            chaptersUrl = {}
            count = 0
            for i in urls:
                # chaptersUrl[count] = "http://biquto.com%s" % i
                a = self.url.split('/')
                b = i.split('/')
                if len(a[-1]) == 0:
                    a = a[:-1]
                if len(b[0]) == 0:
                    b = b[1:]
                urlTemp = ''
                print(a)
                print(b)
                for i in a:
                    if i != b[0]:
                        if i == "index.html":
                            break
                        urlTemp = urlTemp + i + '/'
                        print(urlTemp)
                    else:
                        break

                for c in range(len(b)):

                    if c == len(b) - 1:
                        urlTemp = urlTemp + b[c]
                        print(urlTemp)
                        break
                    else:
                        urlTemp = urlTemp + b[c] + '/'

                chaptersUrl[count] = urlTemp

                count += 1
            return chaptersUrl
        if requestCode == 2:
            title = element.xpath(self.xpathOfTitle)
            if title:
                title = title[0]
            else:
                title = "None"

            # text = element.xpath("//div[@id='content']/p/text()")
            text_ = element.xpath(self.xpathOfText)
            text = []
            for i in text_:
                if i != "\r" or "\n":
                    text.append("".join(i))
            if text:
                # print(title,text)
                return title, text
            else:
                return title, ["None"]

    def downloader(self, sequence, url):
        global document, finishedNum
        response = self.gethtml(url)
        if response:
            html = response.read().decode(self.code)
            data = self.parseHtml(html, 2)
            document[sequence] = data
            finishedNum += 1
            print("\r%d/%d" % (finishedNum, len(chaptersUrl)), end='')
            return data
        pass


def test():
    global chaptersUrl
    app = App(url='http://www.liehuozw.com/0/142/', code='GBK',
              xpathOfNovelName='/html/body/div/div[3]/div/div[2]/h1/text()',
              xpathOfChaptersUrl='/html/body/div/div[6]/div[1]/div[2]/ul/li/a/@href',
              xpathOfTitle="//div[@class='nr_title']/h3/text()",
              xpathOfText="//p[@class='articlecontent']/text()")
    # html = app.gethtml('http://www.liehuozw.com/0/142//87885.html').read().decode("gbk")

    name, chaptersUrl = app.parseHtml( requestCode=0)
    print(name)
    print(chaptersUrl)
    document = {}
    threadPool = ThreadPoolExecutor(5)
    '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive
Cookie: __cfduid=dfba78195a1f593d53a8f0a3b265395131568875117; UM_distinctid=16d483e8cbb50b-0a4437aa6d8d54-5373e62-1fa400-16d483e8cbc841; CNZZDATA1274272693=451969334-1568872824-%7C1574683169; jieqiVisitId=article_articleviews%3D142
Host: www.liehuozw.com
Referer: http://www.liehuozw.com/0/142/
Upgrade-Insecure-Requests: 1'''
    app.header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "__cfduid=dfba78195a1f593d53a8f0a3b265395131568875117; UM_distinctid=16d483e8cbb50b-0a4437aa6d8d54-5373e62-1fa400-16d483e8cbc841; CNZZDATA1274272693=451969334-1568872824-%7C1574606096; jieqiVisitId=article_articleviews%3D142",
        "Host": "www.liehuozw.com",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://www.liehuozw.com/0/142/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    for i in sorted(chaptersUrl.keys()):
        print(chaptersUrl[i])
        threadPool.submit(app.downloader, i, chaptersUrl[i])
    threadPool.shutdown()
    with open(name, "wb") as f:
        pickle.dump(document, f)

    # code = "utf-8"
    # response = app.gethtml("http://www.shuquge.com/txt/8659/index.html")
    # if response:
    #     if 'Content-Encoding' in response.info() and response.info()['Content-Encoding'] == 'gzip':
    #         print("gzip decompress")
    #         html = gzip.decompress(response.read()).decode(code, errors="ignore")
    #     else:
    #         html = response.read().decode(code, errors="ignore")
    #     name,chaptersUrl=app.parseHtml(html,0)
    #     print(name)
    #     print(chaptersUrl)


if __name__ == '__main__':
    test()
    exit()
    # # app = App(url='http://www.shuquge.com/txt/8659/index.html',
    # #           xpathOfNovelName='//h2/text()',
    # #           xpathOfChaptersUrl='/html/body/div[5]//dd/a/@href',
    # #           xpathOfTitle='//*[@id="wrapper"]/div[4]/div[2]/h1/text()',
    # #           xpathOfText='//*[@id="content"]/text()')
    # app = App(url='http://www.liehuozw.com/0/142/',
    #           xpathOfNovelName='/html/body/div/div[3]/div/div[2]/h1/text()',
    #           xpathOfChaptersUrl='/html/body/div/div[6]/div[1]/div[2]/ul/li/a/@href',
    #           xpathOfTitle="//div[@class='nr_title']/h3/text()",
    #           xpathOfText="//p[@class='articlecontent']/text()")
    # code = "utf-8"
    # app.header = {
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    #     "Accept-Encoding": "gzip, deflate",
    #     "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    #     "Cookie": "__cfduid=dfba78195a1f593d53a8f0a3b265395131568875117; UM_distinctid=16d483e8cbb50b-0a4437aa6d8d54-5373e62-1fa400-16d483e8cbc841; CNZZDATA1274272693=451969334-1568872824-%7C1574606096; jieqiVisitId=article_articleviews%3D142",
    #     "Host": "www.liehuozw.com",
    #     "Proxy-Connection": "keep-alive",
    #     "Upgrade-Insecure-Requests": "1"}
    # threadPool = ThreadPoolExecutor(10)
    # # response = app.gethtml("http://biquto.com/50260/")
    # response = app.gethtml("http://www.shuquge.com/txt/8659/index.html")
    # document = {}
    # if response:
    #     if 'Content-Encoding' in response.info() and response.info()['Content-Encoding'] == 'gzip':
    #         print("gzip decompress")
    #         html = gzip.decompress(response.read()).decode(code, errors="ignore")
    #     else:
    #         html = response.read().decode(code)
    #     print(html)
    #
    #     name = app.parseHtml(html, 0)
    #     print(name)
    #     chaptersUrl = app.parseHtml(html, 1)
    #     finishedNum = 0
    #     for i in sorted(chaptersUrl.keys()):
    #         print(i, chaptersUrl[i])
    #         continue
    #         threadPool.submit(app.downloader, i, chaptersUrl[i])
    #     threadPool.shutdown()
    #     print("download finished")
    #     with open(name, "wb") as f:
    #         pickle.dump(document, f)
    #     # string = ""
    #     # for i in sorted(document.keys()):
    #     #     title = document[i][0]
    #     #     text = document[i][1]
    #     #     string = string + title + "\n"
    #     #     for txt in text:
    #     #         string = string + txt + "\n"
    #     # with open("%s.txt" % name, 'w') as f:
    #     #     f.write(string)
