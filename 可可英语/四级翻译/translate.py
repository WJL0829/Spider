
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}

def remove2next1(string):
    treated_content = re.sub('\n\n', '\n', string, flags=re.S + re.I)
    return treated_content

def get_html(url):
    response = requests.get(url, headers=headers)
    # 表示网络请求成功的意思，返回200这个状态表示已经获取到数据了
    if response.status_code == 200:
        response.encoding = 'utf-8'
        # print(response.apparent_encoding)
        return response.text

def parse_text(html):
    # 将页面解析为BeautifulSoup对象
    soup = BeautifulSoup(html, 'lxml')

    # select获取所有满足查询条件的记录
    title = soup.select('div.f-title')[0].string
    content = soup.select('#content > div > div.infoMain > div.f-y.w.hauto')[0]
    texts = content.select('p')

    result = ''
    for text in texts:
        result += text.get_text()
    result_text = remove2next1(result)
    return title, result_text

def parse_index(html):
    soup = BeautifulSoup(html, 'lxml')
    links = soup.select('.listItem')

    srcs = []
    for link in links:
        src = link.select('a')[0]['href']
        src = 'http://m.kekenet.com' + src
        srcs.append(src)
    return srcs

def get_index(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        # print(response.apparent_encoding)
        return response.text

def save_text(title, content):
    with open(title + '.txt', 'a', encoding='utf-8') as f:
        f.write(content)
        f.close()



def downloadFILE(url, name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    }
    resp = requests.get(url=url, stream=True, headers=headers)
    content_size = int(int(resp.headers['Content-Length']) / 1024)
    with open(name, "wb") as f:
        print("Pkg total size is:", content_size, 'k,start...')
        for data in tqdm(iterable=resp.iter_content(1024), total=content_size, unit='k', desc=name):
            f.write(data)
        print(name, "download finished!")


if __name__ == "__main__":
    # for i in range(1, 29):
    for i in range(1, 14):
        # url = 'http://m.kekenet.com/cet4/f/fd/List_{}.shtml'.format(str(i))
        url = 'http://m.kekenet.com/cet4/15325/List_{}.shtml'.format(str(i))
        html = get_index(url)
        srcs = parse_index(html)
        print('list', i)
        for src in srcs:
            detial_html = get_html(src)
            title, result_text = parse_text(detial_html)
            save_text(title, result_text)

# 四级翻译备考辅导 http://m.kekenet.com/cet4/f/fd/
# 英语四级翻译模拟题附答案和详解 http://m.kekenet.com/cet4/15325/















