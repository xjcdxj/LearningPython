import time
from urllib import request
from lxml import etree
from multiprocessing import Pool
from threading import Thread, Semaphore, Lock
import os, gc
from fake_useragent import UserAgent


def get_html(url, refer=None, _path=None):
    try:
        rq = request.Request(url)
    except:
        return None
    if _path:
        rq.add_header(':path', _path)
    rq.add_header(
        'Cookie',
        '__cfduid=d5df11827f6f9ce95f27c652d41309e9f1569858273')
    rq.add_header('user-agent',
                  'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                  '/73.0.3683.86 Mobile Safari/537.36')
    if refer:
        rq.add_header('refer', refer)
    count = 0
    while count < 4:
        try:
            response = request.urlopen(rq, timeout=10)
            html = response.read()
            if html:
                return html
            else:
                count += 1
                continue
        except:
            count += 1

    # print('%s failed' % url)
    return None


# def collect(url):
#     try:
#         header = {
#             'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36'
#         }
#         rq = request.Request(url, headers=header)
#         response = request.urlopen(rq)
#         if response.getcode() == 200 or '200':
#             return response.read()
#         else:
#             time.sleep(2)
#             print('%s waiting' % url)
#             return collect(url)
#     except:
#         return None
#
#
# def parseHTML(html, stat):
#     pass


def save(url, keyword):
    # gc.collect()
    global finishedtask
    html = get_html(url)
    if html:
        html = html.decode()
        element = etree.HTML(html)
        pic = element.xpath(
            '//div[@class="single-content"]//div[@class="media-single-content"]/img/@src')  # 详情页的大图片xpath
        pic1 = element.xpath('//div[@class="single-content"]/article//div[@class="entry"]/p/img/@src')
        # del html
        # del element
        # print(pic)
        html = None
        element = None
        if pic or pic1:
            if pic:
                pic = pic[0]
            else:
                pic = pic1[0]

            filename = pic.split('/')[-1]

            html = get_html(pic)
            if html:
                try:
                    with open('%s/%s' % (keyword, filename), 'wb') as f:
                        f.write(html)
                    # print(filename)
                    lock.acquire()
                    finishedtask += 1

                    print('\r正在下载%s,已下载%d张图片' % (filename, finishedtask), end='')
                    lock.release()
                    # del html
                    html = None
                    filename = None
                except:
                    # del html
                    html = None
                    pass
                    # exit()
        else:
            # del html
            html = None
            # print('***%s' % url)
            # exit()
    # del html


def search(keyWord):
    global count
    try:
        os.mkdir(keyWord)
        # os.chdir(keyWord)
    except FileExistsError:
        # os.chdir(keyWord)
        pass
    # existed.appand(os.listdir(keyWord))
    # existed = os.listdir(keyWord)
    try:
        with open('%s/log.txt' % keyWord, 'r') as f:
            url = f.read()
    except FileNotFoundError:
        url = 'https://watchjavonline.com/?s=%s' % keyWord  # keyWord搜索关键字

    while True:
        # print('-------%s-------' % url)
        with open('%s/log.txt' % keyWord, 'w') as f:
            f.write(url)
        html = get_html(url)
        if html:
            html = html.decode()
            # print(html)
            # print(html)
            element = etree.HTML(html)
            # lastPage = element.xpath('/html/body/div[1]/div[1]/div[2]/a[9]/text()')
            AVCoversTemp = element.xpath("//div[@class='content-masonry']/a/@href")  # 封面地址xpath,获得当前页所有的详情页地址列表
            nextPageUrl = element.xpath('//a[@class="nextpostslink"]/@href')
            # del html
            # del element
            html = None
            element = None
            if not AVCoversTemp:
                break
            # AVTitle = element.xpath('//*[@id="post-674967"]/a/img/@alt')
            threads = []
            for each in AVCoversTemp:
                t = Thread(target=save, args=(each, keyWord))
                threads.append(t)
            AVCoversTemp = None
            for t in threads:
                t.start()
            # del html

            for t in threads:
                t.join()
            # del threads
            threads = None
            # 获取下一页地址的xpath；如果没有下一页就结束
            if nextPageUrl:
                url = nextPageUrl[0]
            else:
                break
        else:
            html = None
            lock.acquire()
            count -= 1
            lock.release()
            print('\n%s Failed' % keyWord)
    lock.acquire()
    count -= 1
    lock.release()
    # os.chdir('..')


def main():
    global count
    # https://watchjavonline.com/page/1/?s=jljllf
    try:
        with open('finishedLOG.txt', 'r') as f:
            finished = f.read()
            finished = finished.split(' ')
    except FileNotFoundError:
        finished = []
    # print(finished)
    serchList = ['wife', 'mother', 'mom', 'sis', 'step', 'venu', 'juy', 'jux', 'ntr', 'adn', 'atid', 'cand',
                 'cead',
                 'dopp', 'ap', 'abp', 'aqsh', 'dvaj', 'fset', 'gg', 'gvg', 'hbad', 'havd', 'hunta', 'iptd',
                 'ipx',
                 'ipz', 'juc', 'meyd', 'mide', 'nacr', 'natr', 'ndra', 'ngod', 'nhdta', 'nhdtb', 'ntrd',
                 'oba',
                 'pgd', 'rbd', 'rct', 'sdmu', 'shkd', 'snis', 'sprd', 'vagu', 'vec', 'vrtm', 'wanz', 'cheat',
                 'next',
                 'cuckold', 'son', 'teacher', 'neighbor', 'friend', 'incest', 'game', 'pantyhose', 'father', 'dad',
                 'boss',
                 'fera', 'dvdes', 'dasd', 'rape', 'cesd', 'dandy', 'iqqq', 'mrss', 'mdyd', 'brother', 'husband',
                 'silent',
                 'bride', 'kiss', 'daughter', 'immoral', 'slave', 'subordinate', 'widow', 'married', 'nurse']
    threads = []
    for i in serchList:
        if i in finished:
            pass
            # print('%s has finished' % i)

        else:
            t = Thread(target=search, args=(i,))
            threads.append(t)

    count = 0
    for t in threads:
        t.start()
        count += 1
        # global count
        while True:
            if count > 5:
                time.sleep(5)
            else:
                break


def test():
    key = 'mom'
    search(key)


def clean():
    while True:
        time.sleep(30)
        gc.collect()


if __name__ == '__main__':
    t=Thread(target=clean,args=())
    t.daemon=True
    t.start()
    lock = Lock()
    count = 0
    # existed = []
    finishedtask = 0
    try:
        os.mkdir('C:\Files\watchjavonline')
        os.chdir('C:\Files\watchjavonline')
    except FileExistsError:
        os.chdir('C:\Files\watchjavonline')
    # test()
    existed = []
    main()
