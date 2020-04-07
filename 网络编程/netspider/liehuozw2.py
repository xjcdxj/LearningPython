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
			'__cfduid=d5fe0806c8ed40ca21cd61c77e06d9fd61553747111; UM_distinctid=169c28b6f4893a-00efb81ea20541-7a1437-1fa40'
			'0-169c28b6f49414; CNZZDATA1274272693=2147055861-1553746804-%7C1553759464; jieqiVisitId=article_articleviews%3D'
			'142')
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
	global info_dic, success_num
	existed = os.listdir('.')
	html = get_html(url, refer)
	if not html:
		sem.release()
		exit()
	html_str = html.decode('gbk', 'ignore')

	book_name, book_chapter = parse_html_str(html_str, 2)
	num = len(book_chapter)
	if num > 300:
		sem.release()

		exit()
	out = '?|\\*":<>/'
	for chars in out:
		book_name = book_name.replace(chars, '')
	# book_name = book_name.replace('?' and '|' and '\\' and '*' and '"' and ':' and '<' and '>' and '/', '')
	if book_name + '.txt' in existed:
		print('\n\033[32m %s finished\033[0m' % book_name)
		sem.release()
		exit()
	if book_name in existed:
		os.unlink(book_name)

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
			with open(book_name, 'a', encoding='utf-8') as f:
				f.write(title)
				for line in txt:
					f.write(line)
			count += 1
		except FileNotFoundError:
			count += 1
			continue
		info_dic[book_name] = '%d/%d' % (count, num)
		# print('%s: %d/%d  '%(book_name,count,num),end='')
	try:
		del info_dic[book_name]
	except:
		pass

	sem.release()
	try:
		os.rename(book_name, book_name + '.txt')
		success_num += 1
	except:
		pass


def main():
	a = 'http://www.liehuozw.com/paihang/allvisit_{}.html'
	url = []

	for i in range(30, 80):
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


'''
字典格式 小说名：已下载/总数
'''


def info():
	while True:
		if not prt_stat:
			exit()
		word = ''
		for name in info_dic:
			word = '%s%s:%s  ' % (word, name, info_dic[name])
		print('\r<%s>' % word, end='')
		sleep(1)


def main1():
	a = 'http://www.liehuozw.com/paihang/allvisit_{}.html'
	url = []

	for i in range(1, 2):
		url.append(a.format(i))
	url_num = 1
	count_url = len(url)
	pr_t = Thread(target=info)
	pr_t.start()
	for each_page in url:
		print('\n\033[33m' + each_page + '\033[0m')
		html = get_html(each_page)
		if not html:
			print('\n\033[31m%s failed\033[0m ' % each_page)
			continue
		html_str = html.decode('gbk', 'ignore')
		books = parse_html_str(html_str, 1)
		threads = []
		for each in books:
			t = Thread(target=save, args=(each, each_page))
			threads.append(t)
		for t in threads:
			t.daemon = True
			t.start()
			sem.acquire()
		if url_num == count_url:
			for t in threads:
				t.join()
		url_num += 1


if __name__ == '__main__':
	# info = {}
	# t=Thread(target=output,args=())
	# t.start()
	system = os.name
	success_num = 0
	prt_stat = 1
	if system == 'nt':
		try:
			os.mkdir('C://Users/XuJiacheng/Desktop/novel')
			os.chdir('C://Users/XuJiacheng/Desktop/novel')
		except:
			os.chdir('C://Users/XuJiacheng/Desktop/novel')
		try:
			os.mkdir('porn_novel')
			os.chdir('porn_novel')
		except:
			os.chdir('porn_novel')
	elif system == 'posix':
		try:
			os.mkdir('./porn_novel')
			os.chdir('./porn_novel')
		except:
			os.chdir('./porn_novel')
	sem = Semaphore(10)
	info_dic = {}
	main1()
	prt_stat = 0
	print('\n' + 'saved %d txt file' % success_num)
