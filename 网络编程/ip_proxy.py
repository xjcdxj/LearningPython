import requests
from lxml import etree


def run():
    url = 'https://www.kuaidaili.com/free/inha/%d/'
    _ip_pool = []
    for i in range(1, 4):
        response = requests.get(url % i, headers=header)
        if response.status_code == 200:
            # print(extract_ip(response.text))
            _ip_pool += extract_ip(response.text)
    return _ip_pool


def extract_ip(html):
    _ip_pool = []
    elements = etree.HTML(html)
    data_items = elements.xpath('//*[@id="list"]/table/tbody/tr')
    for item in data_items:
        ip = item.xpath('td[1]/text()')[0]
        port = item.xpath('td[2]/text()')[0]
        _ip_pool.append((ip, port))
    return _ip_pool


if __name__ == '__main__':
    header = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 Edg/80.0.361.69'
    }
    ip_pool = run()
    print(ip_pool)
    ip_test_url = 'http://icanhazip.com/'
    response = requests.get(ip_test_url, headers=header,timeout=(5,15))
    print(response.text)
    if ip_pool:
        for item in ip_pool:
            proxy = {
                'http': 'http://%s:%s' % (item[0], item[1]),
                'https': 'https://%s:%s' % (item[0], item[1])
            }
            print(proxy)
            try:
                response = requests.get(ip_test_url, proxies=proxy, headers=header)
                html = response.text
                if html == item[0]:
                    print('%s:%s passed' % (item[0], item[1]))
                else:
                    print('%s:%s failed, response = %s' % (item[0], item[1], html))
            except:
                print('%s:%s failed' % (item[0], item[1]))
