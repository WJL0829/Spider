import re
import requests
from bs4 import BeautifulSoup

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''


# 分解页面
def parseHTMLText(text,ilt):
    soup = BeautifulSoup(text, 'html.parser')
    aTag = list(soup.find_all('a', target='_blank'))
    path = 'D:\SpiderTest'
    for a in range(len(aTag)):
        ilt.append(aTag[a].string)
        path1 = path + '\ ' + aTag[a].string + '.txt'
        url2 = 'https://www.51voa.com/' + aTag[a].attrs['href']
        storeText(path1, url2)


# 保存页面
def storeText(path,url):
    text = getHTMLText(url)
    soup = BeautifulSoup(text,'html.parser')
    p = soup.find_all('p')
    # 这里返回的不是对应的的string类型，是没有办法直接写入的
    path = path.replace(' ','')
    path = path.replace('?','')
    with open(path,'w') as f:
        for i in range(len(p)):
            f.write(str(p[i].string))


# 将对应的信息输出到控制台
def printMessage(ilt):
    text = '{:<10}\t{:<20}'
    print(text.format("序号", "文章名"))
    count = 1
    for i in ilt:
        print(text.format(count, i))
        count += 1

# 用main函数将所有的程序连接起来
def main():
    url = 'https://www.51voa.com/Technology_Report_1.html'
    i = 4
    res = list()
    for i in range(2,4):
        text = getHTMLText(url)
        parseHTMLText(text,res)
        r = 'Report_'+str(i)
        target = re.findall(r'Report_\d',url)
        url = url.replace(target[0],r,1)
    printMessage(res)

main()