import requests
import urllib.request
from lxml import etree
import re
url='http://fitgirl-repacks.site/call-duty-black-ops-dlcs-zombies-multiplayer/'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
'Referer':'http://fitgirl-repacks.site/all-my-repacks-a-z/?lcp_page0=3#lcp_instance_0'
}
response = requests.get(url, headers=header)
html = response.content.decode()
print(html)
# elements = etree.HTML(html_str)
# game_links=elements.xpath("//ul[@class='lcp_catlist']/li/a/@href")
# name=elements.xpath("//ul[@class='lcp_catlist']/li/a/@title")
# print(name)

# i='magnet:?xt=urn:btih:A68B1757CFA2616E14DA7669604ACCD42DDC4E42'
# data=re.match(r'magnet:\?xt=urn:btih:')





# rq=urllib.request.Request(url)
# rq.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36')
# rq.add_header('Referer','http://fitgirl-repacks.site/all-my-repacks-a-z/?lcp_page0=3#lcp_instance_0')
# response=urllib.request.urlopen(rq)
# html=response.read().decode()

# magnet=re.findall(r'(magnet:\?xt=urn:btih:[a-z|A-Z|1-9]+)"',html)
# print(magnet)
# exit()
elements=etree.HTML(html)
name=elements.xpath("//h1[@class='entry-title']")
print(name)
data=elements.xpath("//h1[@class='entry-title']/text()")
print(data)
exit()
for each in data:
    match = re.match('magnet:\?xt=urn:btih:[\d|a-z|A-Z]+$', each)
    if match:
        print(match.group())




# data=re.findall(r'<a href="(magnet:?xt=urn:btih:.+?)">magnet',html)
# print(data)