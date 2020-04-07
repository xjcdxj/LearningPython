# from bs4 import BeautifulSoup
# import urllib.request
#
# url='https://www.biqukan.com/57_57540/'
# header = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
#     }
# req=urllib.request.Request(url)
# req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36')
# response=urllib.request.urlopen(req).read().decode('gbk')
# # print(response.read().decode('gbk'))
# bs_str=BeautifulSoup(response)
# text=bs_str.find_all('div' ,class_="listmain")
# lin_bs4=BeautifulSoup(str(text[0]))
# links=lin_bs4.find_all('a')
# print(links)
from lxml import etree
import requests


class Downloantext():
    # 获取html数据
    def __init__(self):
        self.url = 'https://www.biqukan.com/57_57540/'

    def get_html(self, url):
        # 获取html数据
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        }
        response = requests.get(url, headers=header)
        html_str = response.content.decode('gbk')
        return html_str

    def each_chapter_link(self, html_str):

        html = etree.HTML(html_str)
        temp_links = html.xpath("//div[@class='listmain']/dl/dd/a/@href")

        links = ['https://www.biqukan.com{}'.format(i) for i in temp_links]
        links.sort()
        set_temp = set(links)
        links = list(set_temp)
        links.sort()

        return links

    def parse_chapter(self, html_str):
        text = {}
        chapter_html = etree.HTML(html_str)
        txt_temp = chapter_html.xpath("//div[@class='showtxt']//text()")
        title = chapter_html.xpath("//div[@class='content']/h1/text()")[0]
        save_txt = []

        for tt in txt_temp:
            tt = "".join(tt.split())
            save_txt.append(tt)

        text[title] = save_txt

        return text  # 返回一个字典，字典键值对是标题和内容
    def save(self,text):
        f=open('yyy.txt','a')
        for i in text:
            f.write(i+'\n')
            for each in text[i]:
                f.write(' '*8+each+'\n')
        f.close()

    # 主逻辑
    def run(self):
        # 1访问网页获取数据
        html_str = self.get_html(self.url)
        # 2从数据中心解析出每章地址
        links = self.each_chapter_link(html_str)
        # 循环
        while len(links) > 0:
            # 3访问每章地址得到数据
            for each in links:
                chapter_html_str = self.get_html(each)

                # 4解析每章网页数据，得到正文和章节名
                text = self.parse_chapter(chapter_html_str)
                #5保存到文件
                self.save(text)



def main():
    down = Downloantext()
    down.run()


if __name__ == '__main__':
    main()

# url='https://www.biqukan.com/57_57540/'
# header = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
#     }
# req=urllib.request.Request(url)
# req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36')
# response=urllib.request.urlopen(req).read().decode('gbk')
# element=etree.HTML(response)
# title=element.xpath("//div[@class='listmain']/dl/dd//text()")
#
# print(links)
