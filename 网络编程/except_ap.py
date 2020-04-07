from urllib import request
from lxml import etree
from multiprocessing import Pool
from threading import Thread, Semaphore
import os
from time import sleep


def get_html(url, refer=None, _path=None):
    rq = request.Request(url)
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


def save(pic_url, detail_url):
    global existed
    # existed = os.listdir()

    filename = pic_url.split('/')[-2]
    if filename+'.jpg' in existed:
        print('%s existed'%filename)
        exit()
    html = get_html(pic_url)
    if not html:
        exit()
    with open(filename + '.jpg', 'ab') as f:
        f.write(html)
    with open(search + '.txt', 'a') as f:
        f.write(filename + ':' + detail_url + '\n')
    existed.append(filename+'.jpg')
    print(filename + ' success')


if __name__ == '__main__':
    try:
        os.mkdir('C://watchjavongline')
        os.chdir('C://watchjavongline')
    except:
        os.chdir('C://watchjavongline')
    existed = os.listdir()
    serlist = [
        'wife', 'mother', 'mom', 'sis', 'step', 'venu-', 'juy-', 'jux-', 'ntr-', 'adn-', 'atid-', 'cand-', 'cead-',
        'dopp-', 'abp-', 'aqsh-', 'dvaj-', 'fset-', 'gg-', 'gvg-', 'hbad-', 'havd-', 'hunta-', 'iptd-', 'ipx-',
        'ipz-',
        'juc-', 'meyd-', 'mide-', 'nacr-', 'natr-', 'ndra-', 'ngod-', 'nhdta-', 'nhdtb-', 'ntrd-', 'oba-', 'pgd-',
        'rbd',
        'rct-', 'sdmu-', 'shkd-', 'snis-', 'sprd-', 'vagu-', 'vec-', 'vrtm-', 'wanz-', 'cheat', 'next', 'cockold',
        'son',
        'teacher', 'neighbor', 'friend', 'incest', 'game', 'pantyhose', 'father', 'dad'
    ]
    serlist = set(serlist)
    serlist = list(serlist)
    for search in serlist:
        print(search)
        # try:
        #     os.mkdir(search)
        #     os.chdir(search)
        # except:
        #     os.chdir(search)

        url = 'https://watchjavonline.com/?s={}'.format(search)
        html = get_html(url, 'https://watchjavonline.com/')
        html_str = html
        if not html_str:
            print('%s failed'%search)
            continue

        element = etree.HTML(html_str)
        try:
            last = element.xpath("//div[@class='wp-pagenavi']/a[@class='last']/@href")[0]
            maxnum = last.split('/')[-2]
            # last = int(last)
            maxnum = int(maxnum)
        except IndexError:
            maxnum = 1

        print('maxpage:%d' % maxnum)
        for num in range(1, maxnum + 1):
            print('search for %s; page %d/%d' % (search, num, maxnum))
            '''https://watchjavonline.com/page/1/?s=jux'''
            url = 'https://watchjavonline.com/page/{}/?s={}'.format(num, search)
            refer = 'https://watchjavonline.com/page/{}/?s={}'.format(num - 1, search)
            _path = '/page/%d/?s=%s' % (num, search)
            html = get_html(url, refer)
            if not html:
                continue
            element = etree.HTML(html)
            pic_links = element.xpath("//div[@class='post-bodycopy clearfix']/p/img/@src")
            if not pic_links:
                continue
            detail_links = element.xpath("//div[@class='post-headline']/h2/a/@href")
            all_av = dict(zip(pic_links, detail_links))
            threads = []

            for each_av in all_av:
                pic_url = each_av
                detail_url = all_av[each_av]
                t = Thread(target=save, args=(pic_url, detail_url))
                threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        # os.chdir('C://watchjavongline')
