from urllib import request
from lxml import etree
from multiprocessing import Pool
from threading import Thread, Semaphore
import os
from time import sleep


def get_html(url, refer=None):
    rq = request.Request(url)
    rq.add_header(
        'Cookie',
        '__cfduid=d5fe0806c8ed40ca21cd61c77e06d9fd61553747111; UM_distinctid=169c28b6f4893a-00efb81ea20541-7a1437-1fa400-169c28b6f49414; CNZZDATA1274272693=2147055861-1553746804-%7C1553759464; jieqiVisitId=article_articleviews%3D142')
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

                continue
            return html
        except:
            count += 1

    print('%s failed' % url)
    return None


def parse_html_str(html_str, type):
    element = etree.HTML(html_str)
    # 1:获取小说连接，2：获取章节连接3：获取征文
    if type == 1:
        urls = element.xpath("//p/a/@href")
        url = [urls[i] for i in range(1, len(urls), 2)]
        return url
    if type == 2:
        name = element.xpath("//div[@class='introduce']/h1/text()")[0]
        chapter = element.xpath("//div[@class='ml_list']//li/a/@href")
        return name, chapter
    if type == 3:
        title = element.xpath("//div[@class='nr_title']/h3/text()")[0]
        txt = element.xpath("//p[@class='articlecontent']/text()")
        return title, txt


def save(url, refer):
    existed = os.listdir('.')
    html_str = get_html(url, refer).decode('gbk', 'ignore')
    if not html_str:
        sem.release()
        exit()
    book_name, book_chapter = parse_html_str(html_str, 2)
    num = len(book_chapter)
    if num > 300:
        sem.release()

        exit()
    book_name = book_name.replace('?' and '|' and '\\' and '*' and '"' and ':' and '<' and '>' and '/' and '*', '')
    if book_name + '.txt' in existed:
        print('%s finished' % book_name)
        sem.release()
        exit()
    if book_name in existed:
        os.unlink(book_name)
    print(book_name)

    count = 0
    for each_chapter in book_chapter:
        chapter_url = url + each_chapter
        html = get_html(chapter_url, url)
        if not html:
            count += 1
            continue
        html_str = html.decode('gbk', 'ignore')

        title, txt = parse_html_str(html_str, 3)
        try:
            with open( book_name, 'a', encoding='utf-8') as f:
                f.write(title)
                for line in txt:
                    if line:
                        f.write(line)
        except FileNotFoundError:
            count += 1
            continue

        # print('%s: %d/%d  '%(book_name,count,num),end='')
    sem.release()
    try:
        os.rename(book_name,book_name + '.txt')
    except:
        pass


def main():
    a = 'http://www.liehuozw.com/paihang/allvisit_{}.html'
    url = []

    for i in range(1, 20):
        url.append(a.format(i))
    for each_page in url:
        print(each_page)
        pool = Pool(3)
        html = get_html(each_page)
        if not html:
            continue
        html_str = html.decode('gbk', 'ignore')
        books = parse_html_str(html_str, 1)
        # threads=[]
        # for each in books:
        #     t=Thread(target=save,args=(each_book,each_page))
        #     threads.append(t)
        # while len(books):
        #     flag=True
        #     while flag:
        #         t=
        for each_book in books:
            print(each_book)

            pool.apply_async(save, (each_book, each_page))
        pool.close()
        print('*****')
        pool.join()


def main1():
    a = 'http://www.liehuozw.com/paihang/allvisit_{}.html'
    url = []

    for i in range(1, 20):
        url.append(a.format(i))
    sun = 1
    cc = len(url)
    for each_page in url:
        print(each_page)
        html = get_html(each_page)
        if not html:
            print('%s failed ' % each_page)
            continue
        html_str = html.decode('gbk', 'ignore')
        books = parse_html_str(html_str, 1)
        threads = []
        for each in books:
            t = Thread(target=save, args=(each, each_page))
            threads.append(t)
        for t in threads:
            print('++++++++++')
            t.start()
            sem.acquire()
        if sun == cc:
            for t in threads:
                t.join()
        sun += 1


if __name__ == '__main__':
    # info = {}
    # t=Thread(target=output,args=())
    # t.start()
    try:
        os.mkdir('D://小说/烈火中文')
        os.chdir('D://小说/烈火中文/')
    except:
        os.chdir('D://小说/烈火中文/')
    sem = Semaphore(5)
    main1()
