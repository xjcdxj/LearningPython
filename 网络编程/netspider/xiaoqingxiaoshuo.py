from urllib import request
from threading import Thread, Semaphore, activeCount
from lxml import etree
import os
import time
from multiprocessing import Pool


class Download(object):
    def __init__(self):
        self.sem = Semaphore(4)
        self.complete_ratio_info1 = {}
        self.theads_num = 1
        pass

    def _print(self):
        while True:
            num = activeCount()
            doc = ''
            if self.complete_ratio_info1:
                for i in self.complete_ratio_info1:
                    doc = doc + self.complete_ratio_info1[i] + '   '
                print('\r%s  running %d threads' %
                      (doc, self.theads_num), end='')
            time.sleep(1)

    def get_html(self, url, refer=None):
        rq = request.Request(url)
        rq.add_header(
            'cookie', '__cfduid=dcdbb8756489b90242bc37d7f58684dfe1550717555')
        rq.add_header('user-agent',
                      'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36')
        if refer:
            rq.add_header('refer', refer)
        count = 0
        while count < 4:
            try:
                response = request.urlopen(rq, timeout=10)
                html = response.read()
                if html == 0:
                    count += 1
                    print('\033[1;31m \n%s failed, retry %d\033[0m!' %
                          (url, count))
                    continue
                return html
            except:
                count += 1
                print('\033[1;31m \n%s timeout, retry %d\033[0m!' %
                      (url, count))
        print('%s failed' % url)
        return None

    def parse_html_str(self, html_str, type):
        # type 0获取每本小说，1获取小说章节 2 获取小说征文,3 name
        elements = etree.HTML(html_str)
        if type == 0:
            each_novel_urls = elements.xpath(
                "//span[@class='s2']/a[@target='_blank']/@href")
            return each_novel_urls
        elif type == 1:
            each_chapter_temp = elements.xpath("//dd/a/@href")
            each_chapter = [
                'http://www.xiaoqiangxs.org{}'.format(i) for i in each_chapter_temp]
            del each_chapter_temp
            return each_chapter
        elif type == 2:
            chapter_title = elements.xpath(
                "//div[@class='bookname']/h1/text()")[0]
            chapter_txt = elements.xpath("//div[@id='content']/text()")
            return chapter_title, chapter_txt
        elif type == 3:
            name = elements.xpath("//div[@id='info']/h1/text()")
            return name

    def save(self, novel_url, refer):
        dir = 'D://小说'
        novel_html_str = self.get_html(
            novel_url, refer).decode('gbk', 'ignore')
        if novel_html_str == 0:
            print('\033[1;31m%s failed\033[0m!' % novel_url)
            self.theads_num -= 1
            # self.sem.release()
        novel_name = self.parse_html_str(novel_html_str, 3)[0]
        exisited = os.listdir(dir)
        if novel_name + '.txt.temp' in exisited:
            os.unlink(dir + '/' + novel_name + '.txt.temp')
        if novel_name + '.txt' not in exisited:
            # print('\n' + novel_name)

            # 获取小说章节

            # 每章地址
            chapter_url = self.parse_html_str(novel_html_str, 1)
            num = len(chapter_url)
            count = 1
            for each_chapter in chapter_url:
                try:
                    chapter_html_str = self.get_html(
                        each_chapter, novel_url).decode('gbk', 'ignore')
                except:
                    continue
                if chapter_html_str == 0:
                    print('\033[1;31m%s failed\033[0m!' % each_chapter)
                    continue
                chapter_title, chapter_txt = self.parse_html_str(
                    chapter_html_str, 2)
                try:
                    with open(dir + '/' + novel_name + '.txt.temp', 'a', encoding='utf-8') as f:

                        f.write(chapter_title + '\n')
                        for each_line in chapter_txt:
                            f.write(each_line + '\n')
                except:
                    count += 1
                    self.complete_ratio_info1[novel_name] = '%s：%d/%d' % (
                        novel_name, count, num)
                    continue
                self.complete_ratio_info1[novel_name] = '%s：%d/%d' % (
                    novel_name, count, num)
                count += 1
                # print('\r%s %d/%d' % (novel_name, count, num), end='')
            try:
                os.rename(dir + '/' + novel_name + '.txt.temp',
                          dir + '/' + novel_name + '.txt')
            except:
                pass

            finally:
                self.theads_num -= 1
                del self.complete_ratio_info1[novel_name]
                # self.sem.release()
        else:
            print(novel_name + ' finished' +
                  '%d threads running' % self.theads_num)
            # self.sem.release()
            pass
            # self.sem.release()

            # print('\n' + novel_name)
            # try:
            #     # 获取小说章节
            #
            #     # 每章地址
            #     chapter_url = self.parse_html_str(novel_html_str, 1)
            #     num = len(chapter_url)
            #     count = 1
            #     for each_chapter in chapter_url:
            #         chapter_html_str = self.get_html(each_chapter, novel_url).decode('gbk')
            #         chapter_title, chapter_txt = self.parse_html_str(chapter_html_str, 2)
            #
            #         with open(dir + '/' + novel_name, 'a', encoding='utf-8') as f:
            #             f.write(chapter_title + '\n')
            #             for each_line in chapter_txt:
            #                 f.write(each_line + '\n')
            #         # self.complete_ratio_info1[novel_name] = '%s：%d/%d' % (novel_name, count, num)
            #         count += 1
            #         print('\r%s %d/%d' % (novel_name, count, num), end='')
            #     os.rename(dir + '/' + novel_name, dir + '/' + novel_name + '.txt')
            #     # self.sem.release()
            # except:
            #     print('\n%s failed' % novel_name)
            # self.complete_ratio_info1[novel_name] = 'failed'
            # self.sem.release()

    def thread_run(self):
        # 1生成网页地址
        dir = 'D://小说'
        try:
            os.mkdir(dir)
        except:
            pass
        url = [
            'http://www.xiaoqiangxs.org/wanben/1_{}'.format(i) for i in range(1, 37)]
        t1 = Thread(target=self._print)
        t1.start()
        for each_page in url:
            # 2打开网页获取数据
            print(each_page + '：')
            html_str = self.get_html(each_page).decode('gbk', 'ignore')
            each_novel_urls = self.parse_html_str(html_str, 0)
            threads = []
            for each_novel in each_novel_urls:
                # try:
                #     self.save(each_novel, each_page)
                # except:
                #     pass
                # 多线程 每本小说
                t = Thread(target=self.save, args=(each_novel, each_page))
                threads.append(t)
            while len(threads):
                while self.theads_num < 2:
                    t = threads.pop()
                    t.start()
                    self.theads_num += 1
                time.sleep(0.5)

            # for t in threads:
            #     if self.theads_num>5:
            #         time.sleep(1)
            #     t.start()
            #     del threads[t]
            #     self.theads_num+=1

            # self.sem.acquire()
            # for t in threads:
            #     t.join()

        pass

    def process_run(self):
        dir = 'D://小说'
        try:
            os.mkdir(dir)
        except:
            pass
        url = [
            'http://www.xiaoqiangxs.org/wanben/1_{}'.format(i) for i in range(1, 37)]
        t1 = Thread(target=self._print)
        t1.start()
        for each_page in url:
            pool = Pool(3)
            # 2打开网页获取数据
            print(each_page + '：')
            html_str = self.get_html(each_page).decode('gbk', 'ignore')
            each_novel_urls = self.parse_html_str(html_str, 0)
            num = 0
            for each_novel in each_novel_urls:
                pool.apply_async(self.save, (each_novel,))
                print(num)
                num += 1
            pool.close()
            pool.join()


def main():
    download = Download()
    download.thread_run()


def test():
    download = Download()
    download.save('http://www.xiaoqiangxs.org/1_1073/',
                  'http://www.xiaoqiangxs.org/wanben/1_1')


if __name__ == '__main__':
    main()
