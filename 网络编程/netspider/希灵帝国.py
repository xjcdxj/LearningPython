from urllib import request
import re
from lxml import etree
from multiprocessing import Pool
from threading import Thread, Semaphore
import os
from time import sleep


def get_html(url, refer=None):
    rq = request.Request(url)
    # rq.add_header(
    #     'Cookie',
    #     '__cfduid=d5fe0806c8ed40ca21cd61c77e06d9fd61553747111; UM_distinctid=169c28b6f4893a-00efb81ea20541-7a1437-1fa400-169c28b6f49414; CNZZDATA1274272693=2147055861-1553746804-%7C1553759464; jieqiVisitId=article_articleviews%3D142')
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

# url='https://www.biqushu.com/book_8825/4168508.html'
# while True:
#
#     html = get_html(url)
#     html=html.decode('gbk')
#     element=etree.HTML(html)
#     text=element.xpath('//*[@id="htmlContent"]/text()')
#     title=element.xpath('//*[@id="content"]/h1/text()')[0]
#     nextChapter=element.xpath('//*[@id="content"]/div[3]/span[4]/a/@href')[0]
#
#     print(title)
#
#     with open('希灵帝国.txt','a',encoding='utf-8-sig') as f:
#         f.write(title+'\n')
#         for i in text:
#
#             f.write(u'%s'%i+'\n')
#     if nextChapter=='https://www.biqushu.com/book_8825/':
#         break
#     url=nextChapter

text=[]
with open('希灵帝国.txt','r',encoding='utf-8') as f :
    while True:
        t=f.readline()
        if len(t)==0:
            break
        if len(t)==1:
            pass
        else:
            # t=re.sub('\s+','  ',t)


            text.append(t)
            # text.append(t)

with open('xx.txt','a',encoding='utf-8') as g:
    for i in text:
        g.write(i)
