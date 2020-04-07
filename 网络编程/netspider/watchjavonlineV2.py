from urllib import request
from lxml import etree
from multiprocessing import Pool
from threading import Thread, Semaphore, Lock
import os


def get_html(url, refer=None, _path=None):
    try:
        rq = request.Request(url)
    except:
        return None
    if _path:
        rq.add_header(':path', _path)
    rq.add_header(
        'Cookie',
        '__cfduid=dcbe4587f54b4167bc1edeec96eb7ffbc1553860637; _ga=GA1.2.832886922.1553860676')
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
            if html == 0:
                count += 1

                continue
            return html
        except:
            count += 1

    # print('%s failed' % url)
    return None


def save(search, pic_url, detail_url):
    global existed
    existed = os.listdir()

    filename = pic_url.split('/')[-2] + '.jpg'
    if filename in existed:
        print('%s existed' % filename)
    else:
        # if filename+'.jpg' in finished:
        #     #     print('%s existed'%filename)
        #     #     exit()
        html = get_html(pic_url)
        if not html:
            exit()
        try:
            with open(filename, 'wb') as f:
                f.write(html)
        except:
            pass
        # with open(search + '.txt', 'a') as f:
        #     f.write(filename + ':' + detail_url + '\n')
        existed.append(filename)
        # lock.acquire()
        #     #     # # finished.append(filename+'.jpg')
        #     #     # lock.release()
        print(filename + ' success')


def main(search):
    # 创建search文件夹并切换进入文件夹
    print(search)

    try:
        os.mkdir(search)
        os.chdir(search)
    except:
        os.chdir(search)
    existed = os.listdir()
    # 获取搜索也得数据
    url = 'https://watchjavonline.com/?s={}'.format(search)
    html = get_html(url, 'https://watchjavonline.com/')
    html_str = html

    if not html_str:
        print('%s failed' % search)

    else:
        element = etree.HTML(html_str)
        try:
            # last搜索页的最大页面数，使用xpath
            last = element.xpath("//a[@class='last']/@href")

            # 分离出最大数的字符串
            maxnum = last.split('/')[-2]
            # last = int(last)
            maxnum = int(maxnum)
        except IndexError:
            # 如果index错误，说明没有最大页面数，那么就默认只有一页
            maxnum = 1

        print('maxpage:%d' % maxnum)
        # 搜索名称文件下的finished.txt文件，里面记录已经下载过得页面数，没有则默认0
        try:
            with open('finished.txt', 'r') as f:
                finished = f.read()
            finished = int(finished)
        except FileNotFoundError:
            finished = 0
        print('%d has finished' % finished)

        for num in range(finished + 1, maxnum + 1):
            print('search for %s; page %d/%d' % (search, num, maxnum))
            '''https://watchjavonline.com/page/1/?s=jux'''
            # url = 'https://watchjavonline.com/page/{}/?s={}'.format(num, search)
            # refer = 'https://watchjavonline.com/page/{}/?s={}'.format(num - 1, search)
            _path = '/page/%d/?s=%s' % (num, search)
            html = get_html(url)  # 获取搜索页面数为num的页面html
            if not html:
                continue
            element = etree.HTML(html)
            # 获取页面的图片地址和其详情页地址
            pic_links = element.xpath("//div[@class='wrap-content']//li/a/img/@src")
            if not pic_links:
                continue
            # detail_links = element.xpath("//div[@class='post-headline']/h2/a/@href")
            detail_links = None
            # 组成图片链接：详情地址的字典
            all_av = dict(zip(pic_links, detail_links))
            threads = []

            for each_av in all_av:
                pic_url = each_av
                if pic_url.endswith('jpg'):
                    detail_url = all_av[each_av]
                    t = Thread(target=save, args=(search, pic_url, None))
                    threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            with open('finished.txt', 'w') as f:
                f.write(str(num))
        os.chdir('..')
        with open('log.txt', 'a') as f:
            f.write(search + '\n')
        pass


if __name__ == '__main__':
    try:
        os.mkdir('D://log')
    except:
        pass
    try:
        os.mkdir('D://watchjavonline')
        os.chdir('D://watchjavonline')
    except:
        os.chdir('D://watchjavonline')

    serlist = [
        'wife', 'mother', 'mom', 'sis', 'step', 'venu-', 'juy-', 'jux-', 'ntr-', 'adn-', 'atid-', 'cand-', 'cead-',
        'dopp-', 'ap-', 'abp-', 'aqsh-', 'dvaj-', 'fset-', 'gg-', 'gvg-', 'hbad-', 'havd-', 'hunta-', 'iptd-', 'ipx-',
        'ipz-', 'juc-', 'meyd-', 'mide-', 'nacr-', 'natr-', 'ndra-', 'ngod-', 'nhdta-', 'nhdtb-', 'ntrd-', 'oba-',
        'pgd-', 'rbd', 'rct-', 'sdmu-', 'shkd-', 'snis-', 'sprd-', 'vagu-', 'vec-', 'vrtm-', 'wanz-', 'cheat', 'next',
        'cuckold', 'son', 'teacher', 'neighbor', 'friend', 'incest', 'game', 'pantyhose', 'father', 'dad', 'boss',
        'fera-', 'dvdes-', 'dasd', 'rape', 'cesd', 'dandy', 'iqqq', 'mrss', 'mdyd', 'brother', 'husband', 'silent',
        'bride', 'kiss', 'daughter', 'immoral', 'slave', 'subordinate', 'widow', 'married', 'nurse'
    ]

    # finished=[]
    # lock=Lock()
    serlist = set(serlist)
    serlist = list(serlist)
    sstemp = ['shkd-']
    # finished=[]
    # lock=Lock()
    try:
        with open('log.txt', 'r') as f:
            finished = f.read()
        finished = finished.split('\n')
    except FileNotFoundError:
        finished = []
    pools = Pool(4)
    for search in serlist:
        if search in finished:
            print('%s has finished' % search)
            continue

        pools.apply_async(main, (search,))
    pools.close()
    pools.join()
