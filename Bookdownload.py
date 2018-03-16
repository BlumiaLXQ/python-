# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests

"""
类说明:下载小说
Author:沐川

Time:2018-03-16

"""
class downloader(object):
    def __init__(self):
        self.server = 'https://www.23us.cc/html/219/219625/' #想要下载小说的url
        self.target = 'https://www.23us.cc/html/219/219625/'#想要下载小说的章节url
        self.names = []            #存放章节名
        self.urls = []            #存放章节链接
        self.nums = 0            #章节数

    """
    函数说明:获取下载链接
    """
    def get_download_url(self):
        req = requests.get(url = self.target)
        html = req.text
        div_bf = BeautifulSoup(html)
        div = div_bf.find_all('dl', class_ = 'chapterlist')
        a_bf = BeautifulSoup(str(div[0]))
        a = a_bf.find_all('a')
        self.nums = len(a[12:])                                #剔除不必要的章节，并统计章节数
        for each in a[12:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))
            print(self.server + each.get('href'))

    """
    函数说明:获取章节内容
    Parameters:
        target - 下载连接(string)
    Returns:
        texts - 章节内容(string)
    """
    def get_contents(self, target):
        req = requests.get(url = target)
        html = req.text
        bf = BeautifulSoup(html)
        texts = bf.find_all('div', id = 'content')
        texts = texts[0].text.replace('\xa0'*8,'\n\n')
        return texts

    """
    函数说明:将爬取的文章内容写入文件
    Parameters:
        name - 章节名称(string)
        path - 当前路径下,小说保存名称(string)
        text - 章节内容(string)
    """
    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')

if __name__ == "__main__":
    dl = downloader()
    dl.get_download_url()
    print('小说开始下载：')
    print(dl.nums)
    for i in range(dl.nums):
        dl.writer(dl.names[i], '求仙.txt', dl.get_contents(dl.urls[i]))
        print("  已下载:%.3f%%" %  int(i/dl.nums)+ '\r')
    print('小说下载完成')
    '''
if __name__ == '__main__':
    server='https://www.23us.cc/html/219/219625/'
    target = 'https://www.23us.cc/html/219/219625/'
    req = requests.get(url=target)
    html = req.text
    bf = BeautifulSoup(html)
    texts = bf.find_all('dl', class_='chapterlist')
    a_bf = BeautifulSoup(str(texts[0]))
    a = a_bf.find_all('a')
    for each in a:
        print(each.string, server + each.get('href'))
    '''