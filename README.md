标记[wjl]的为原创

# Spider

## 1、猫眼电影TOP100

> 数据来源：http://maoyan.com/board/4

### 代码文件

* MaoYanMovie.py

### 运行结果

* result.txt


利用正则表达式进行匹配，繁琐易错  
解决：利用BeautifulSoup


## 2、今日头条街拍图片

> 数据来源：https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D  


### 代码文件

* toutiao.py

img文件夹中是部分结果

## 3、51VOA文章   

> 数据来源：https://www.51voa.com/  
> 网站源码差不多，稍微修改一下就能用


### 代码文件  

* voa.py：来自网络，可运行   

* [wjl]wjlvoa.py：根据“可可英语”的爬虫文件修改的，修改的点在于对于网址的提取+对内容的匹配

### 运行结果   

51VOA.zip：选取VOA某类文章的第一页，共爬取了50条数据
