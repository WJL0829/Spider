"""
1.音频和所需的文本都在网页源代码中
2.音频直接beautifulsoup解析到链接即可
3.文本的采集稍微麻烦一点，因为位置不固定，只能采集上一层标签，而且需要的p标签中还有span标签中的内容不需要，strong标签不需要，</br>换成换行符
4.解决3的问题采用正则表达式，先把tag类型转成str,删除span标签及其中的内容，删除strong标签，</br>换成换行符，然后转回tag类型，循环遍历p标签，get_text()只取内容，把所用的内容拼接起来保存
"""

import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}


def remove_span_tag(tag):
    content = str(tag)
    # pattern：<span.*?span>表示匹配到第一个span>就停止
    # repl：将span标签和其中的内容全部用''替代，相当于全部删除
    # string：要被处理的那个string字符串
    # re.S + re.I：使.匹配包括换行在内的所有字符  使匹配对大小写不敏感
    treated_content = re.sub('<span.*?span>', '', content, flags=re.S + re.I)
    # 解析出网站的html代码
    result = BeautifulSoup(treated_content, 'lxml')
    return result


def remove_strong_tag(tag):
    content = str(tag)
    treated_content = re.sub('<strong>|<strong/>', '', content, flags=re.S + re.I)
    result = BeautifulSoup(treated_content, 'lxml')
    return result


def remove2next1(string):
    treated_content = re.sub('\n\n', '\n', string, flags=re.S + re.I)
    return treated_content


def change_br2next(tag):
    content = str(tag)
    # treated_content = re.sub('<br>','',content,flags=re.S+re.I)
    treated_content = re.sub('<br/>', '\n', content, flags=re.S + re.I)
    result = BeautifulSoup(treated_content, 'lxml')
    return result


def get_html(url):
    response = requests.get(url, headers=headers)
    # 表示网络请求成功的意思，返回200这个状态表示已经获取到数据了
    if response.status_code == 200:
        response.encoding = 'utf-8'
        # print("response.apparent_encoding" + response.apparent_encoding)
        return response.text


def parse_audio_text(html):
    # 将页面解析为BeautifulSoup对象
    soup = BeautifulSoup(html, 'lxml')

    # select获取所有满足查询条件的记录
    title = soup.select('div.f-title')[0].string
    # print("title" + title)
    audio = soup.select('#show_mp3 > audio')[0].source['src']
    # print(audio)

    content = soup.select('#content > div > div.infoMain > div.f-y.w.hauto')[0]
    texts = content.select('p')
    # print("*？*？*？*？**********" + str(texts) + "***？**？**？*?*？***？**？*****")
    """
    print("<<<<<<<<<<")
    test = change_br2next(remove_strong_tag(remove_span_tag(texts[1])))
    print(test)
    print(">>>>>>>>>>>>>>>")"""
    result = ''
    for text in texts:
        print("<**************" + str(text) + "*******************>")
        a = remove_span_tag(text)
        # print("\n&&&&&&&&&&&&&&&&a的内容是： " + a.get_text() + "&&&&&&&&&&&&&&&&&&\n")
        b = remove_strong_tag(a)
        # print("\n@@@@@@@@@@@@@@@@@@@@b的内容是： " + b.get_text() + "@@@@@@@@@@@@@@@@@@@@\n")

        c = change_br2next(b)
        d = c.get_text()
        result += d
        # print("\n&&&&&&&&&&&&&&&&a的内容是： " + a.get_text() + "&&&&&&&&&&&&&&&&&&\n")
        # result += change_br2next(remove_strong_tag(remove_span_tag(text))).get_text()

    # print("\n<:::::::::" + result + ":::::::::>\n\n")
    result_text = remove2next1(result)
    # print("<<result>>" + result_text)
    # print(">>>")
    return title, audio, result_text
    # texts = remove_strong_tag(remove_span_tag(content.select('p')[1]))


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
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }
    resp = requests.get(url=url, stream=True, headers=headers)
    content_size = int(int(resp.headers['Content-Length']) / 1024)
    with open(name, "wb") as f:
        print("Pkg total size is:", content_size, 'k,start...')
        for data in tqdm(iterable=resp.iter_content(1024), total=content_size, unit='k', desc=name):
            f.write(data)
        print(name, "download finished!")


if __name__ == "__main__":
    for i in range(1, 3):
        url = 'http://m.kekenet.com/menu/14439/List_{}.shtml'.format(str(i))
        html = get_index(url)
        srcs = parse_index(html)
        print(srcs)
        print('list', i)
        for src in srcs:
            detial_html = get_html(src)
            title, audio, result_text = parse_audio_text(detial_html)
            title = re.search('第(.*?)期', title, re.S)

            if title:
                title = title.group(1).zfill(3)

            print(audio)
            save_text(title, result_text)
            downloadFILE(audio, title + '.mp3')

# 24链接http://m.kekenet.com/menu/14439/index.shtml

