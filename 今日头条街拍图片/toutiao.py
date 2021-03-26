import requests,re,os
from hashlib import md5
from selenium import webdriver

def get_cookies(url):
    str=''
    options = webdriver.ChromeOptions() # 在浏览器启动前设置加载选项
    options.add_argument('--headless') # 添加启动参数 设置为无界面模式
    browser = webdriver.Chrome(options=options) # 将参数对象传入Chrome中
    browser.get(url)
    for i in browser.get_cookies():
        try:
            name=i.get('name')
            value=i.get('value')
            str=str+name+'='+value+';'
        except ValueError as e:
            print(e)
    return str

def get_page(offset): # get_page()加载单个Ajax请求的结果，唯一变化的参数就是 offset
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
    }
    url='https://www.toutiao.com/api/search/content/'
    try:
        # 利用urlencode()方法构造请求的GET参数，然后用requests请求该链接，若返回状态码为200，则调用response的json()方法将结果转为JSON格式而后返回
        r=requests.get(url,params=params,headers=headers)
        if r.status_code==200:
            return r.json()
        else:
            print('requests get_page error!')
    except requests.ConnectionError:
        return None

def get_images(json):
# 解析方法：提取每条数据的image_detail字段中的每一张图片链接，将图片链接和图片所属标题一并返回，此时可以构造一个生成器
    data=json.get('data')
    if data:
        for i in data:
            if i.get('title'):
                title=re.sub('[\t]','',i.get('title'))
                url=i.get('article_url')
                if url:
                    r=requests.get(url,headers=headers)
                    if r.status_code==200:
                        images_pattern = re.compile('JSON.parse\("(.*?)"\),\n', re.S)
                        result = re.search(images_pattern, r.text)
                        if result:
                            b_url='http://p3.pstatp.com/origin/pgc-image/'
                            up=re.compile('url(.*?)"width',re.S)
                            results=re.findall(up,result.group(1))
                            if results:
                                for result in results:
                                    yield {
                                        'title':title,
                                        'image':b_url+re.search('F([^F]*)\\\\",',result).group(1)
                                    }
                        else:
                            images = i.get('image_list')
                            for image in images:
                                origin_image = re.sub("list.*?pgc-image", "large/pgc-image", image.get('url'))
                                yield {
                                    'image': origin_image,
                                    'title': title
                                }
def save_image(item):
# 实现一个保存图片的方法save_image()，其中item就是get_images()方法返回的一个字典
# 在该方法中，首先根据item的title来创建文件夹，然后请求该图片链接，获取图片的二进制数据，以二进制的形式写入文件
# 图片的名称可以用其内容的MD5值，这样可以去除重复
    img_path = 'img' + os.path.sep + item.get('title')
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    try:
        resp = requests.get(item.get('image'))
        if requests.codes.ok == resp.status_code:
            file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(
                file_name=md5(resp.content).hexdigest(),
                file_suffix='jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(resp.content)
                print('Downloaded image path is %s' % file_path)
            else:
                print('Already Downloaded', file_path)
    except Exception as e:
        print(e,'none123')

def main(offset):
# 构建一个offset数组，遍历offset，提取图片链接并下载
    a = get_page(offset)
    for i in get_images(a):
        save_image(i)

cookies = get_cookies('https://www.toutiao.com')
headers = {
    'cookie': cookies,
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
}

if __name__=='__main__':
    for i in [x*20 for x in range(3)]:
        main(i)


