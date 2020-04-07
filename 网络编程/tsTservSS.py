import requests
from fake_useragent import UserAgent

rq = requests.post('http://httpbin.org/post', headers={'User-Agent', UserAgent().random()},
                   data={'key1': 'value1', 'key2': 'value2'})
print(rq.text)
