from threading import Thread, Semaphore
from urllib import request
from lxml import etree
import os
import time
from fake_useragent import UserAgent


class Download(object):
    def __init__(self):
        self.url = 'https://www.bixia.org/quanben/'
        self.sem = Semaphore(3)
        self.complete_ratio_info1 = {}

    def _print(self):
        while True:
            doc = ''
            for i in self.complete_ratio_info1:
                doc = doc + self.complete_ratio_info1[i] + '   '
            print('\r%s' % doc, end='')
            time.sleep(1)

    def get_html_str(self, url, refer=None):
        rq = request.Request(url)
        rq.add_header(
            'user-agent',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        )
        rq.add_header(
            'cookie',
            '__cfduid=d340c19c12f314eb7e42bc2ee2d4a47851553136499; UM_distinctid=1699e2648ad8c8-0d257b73fe6b61-9333061-144000-1699e2648ae938; CNZZDATA1261165914=1868597110-1553131196-https%253A%252F%252Fwww.baidu.com%252F%7C1553136617'
        )
        if refer:
            rq.add_header('refer', refer)
        try:
            response = request.urlopen(rq, timeout=10)

        except:
            self.sem.release()
            exit()
        html = response.read().decode('utf-8')
        if len(html) == 0:
            self.sem.release()
            exit()
        else:
            return html

    def parse_html_str(self, html_str, type):
        # tyoe是获取小说列表1还是章节列表2还是小说文本3
        elements = etree.HTML(html_str)

        if type == 1:
            # novel_name_list=elements.xpath("//div[@class='topbooks']//li/a/@title")
            novel_url_list = elements.xpath("//div[@class='topbooks']//li/a/@href")
            return novel_url_list
        elif type == 2:
            novel_chapter_list = elements.xpath("//dd/a/@href")[12:]
            novel_name = elements.xpath("//div[@id='info']/h1/text()")[0]
            return novel_name, novel_chapter_list
        elif type == 3:
            chapter_name = elements.xpath("//div[@class='bookname']/h1/text()")[0]
            chapter_txt = elements.xpath("//div[@id='content']/text()")

            return chapter_name, chapter_txt

    def downloading(self, each_novel_url):
        url = 'https://www.bixia.org{}'.format(each_novel_url)
        html_str = self.get_html_str(url, self.url)
        # 3分析数据获得小说章节列表

        novel_name, novel_chapter_list = self.parse_html_str(html_str, 2)
        novel_name = '{}.txt'.format(novel_name)
        count = 1
        num = len(novel_chapter_list)
        for each_chapter_url in novel_chapter_list:
            each_chapter_url = 'https://www.bixia.org{}'.format(each_chapter_url)
            # 4获取每章的数据，分析出正文
            chapter_html_str = self.get_html_str(each_chapter_url, each_novel_url)
            chapter_name, chapter_txt = self.parse_html_str(chapter_html_str, 3)
            with open(novel_name + 'temp', 'a', encoding='utf-8') as f:
                f.write(chapter_name + '\n')
                for each_line in chapter_txt:
                    f.write(each_line + '\n')
            count += 1
            self.complete_ratio_info1[novel_name] = '%s：%d/%d' % (novel_name, count, num)
        os.rename(novel_name + 'temp', novel_name)
        del self.complete_ratio_info1[novel_name]
        self.sem.release()

    # 单线程爬虫
    def run(self):

        # 主逻辑，运行程序
        # 1.打开网页获取数据，并分析数据获取小说连接列表
        html_str = self.get_html_str(self.url)
        if not html_str:
            print('access timeout')
        novel_url_list = self.parse_html_str(html_str, 1)
        # 2访问每个小说的详细信息列表
        for each_novel_url in novel_url_list:
            self.downloading(each_novel_url)
            # url='https://www.bixia.org{}'.format(each_novel_url)
            # html_str=self.get_html_str(url,self.url)
            # #3分析数据获得小说章节列表
            #
            # novel_name,novel_chapter_list=self.parse_html_str(html_str,2)
            # novel_name='{}.txt'.format(novel_name)
            # print(novel_name)
            # count=1
            # num=len(novel_chapter_list)
            # for each_chapter_url in novel_chapter_list:
            #     each_chapter_url='https://www.bixia.org{}'.format(each_chapter_url)
            #     #4获取每章的数据，分析出正文
            #     chapter_html_str=self.get_html_str(each_chapter_url,each_novel_url)
            #     chapter_name,chapter_txt=self.parse_html_str(chapter_html_str,3)
            #     with open(novel_name,'a',encoding='utf-8') as f:
            #         for each_line in chapter_txt:
            #             f.write(each_line)
            #     print('\r%d/%d  %s'%(count,num,chapter_name),end='')
            #     count+=1

            # with open('temp.txt','w',encoding='utf-8') as f:
            #     for i in chapter_txt:
            #         f.write(i)

        # #创建多线程
        # #创建线程池
        # threads=[]
        # for each_novel_url in novel_url_list:
        #     t=Thread(target=self.multi_save_threading,args=(each_novel_url,))
        #     threads.append(t)

    # 多线程爬虫，线程并发数最大三
    def multi_thread_run(self):
        # 主逻辑，运行程序
        # 1.打开网页获取数据，并分析数据获取小说连接列表
        html_str = self.get_html_str(self.url)
        if not html_str:
            print('access timeout')
        novel_url_list = self.parse_html_str(html_str, 1)
        threads = []
        print_thread = Thread(target=self._print, )
        print_thread.start()
        # 2访问每个小说的详细信息列表
        for each_novel_url in novel_url_list:
            t = Thread(target=self.downloading, args=(each_novel_url,))
            threads.append(t)
        for t in threads:
            t.start()
            self.sem.acquire()
        for t in threads:
            t.join()

        #     t = Thread(target=self.downloading, args=(each_novel_url,))
        #     threads.append(t)
        # for t in threads:
        #     t.start()
        # for t in threads:
        #     t.join()


def main():
    try:
        os.mkdir('D://小说')
        os.chdir('D://小说')
    except:
        os.chdir('D://小说')
    download = Download()
    download.multi_thread_run()


if __name__ == '__main__':
    main()
