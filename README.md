***标记[wjl]的为原创***

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


## 3、可可英语  

### (1)The english we talk

> 数据来源：http://m.kekenet.com/menu/14439/index.shtml   

#### 代码文件  

* the_english_we_talk.py  

来源于网络，可以同时下载文字和音频  
因为我进行了多次测试，所以保留了很多print注释  

#### 运行结果   

* data.zip  


### (2)四级翻译

> 数据来源：  

> 四级翻译备考辅导 http://m.kekenet.com/cet4/f/fd/  

> 英语四级翻译模拟题附答案和详解 http://m.kekenet.com/cet4/15325/  

#### 代码文件  

* [wjl]translate.py  

在“the_wenglish_we_talk.py”的基础上我进行了改写，四级翻译两类文章的爬取代码相差不多(网址+页码范围)，通过注释进行了表示

#### 运行结果   

* 备考辅导.zip  
* 模拟题.zip  

 
## 4、51VOA  

> 数据来源：https://www.51voa.com
> VOA网站源码差不多，爬取其他分类文章稍微修改一下就能用

### (1)VOA慢速  

> 数据来源：https://www.51voa.com/Technology_Report_1.html  

#### 代码文件

* [wjl]VOA慢速.py：我在可可英语爬虫文件的基础上改写  

* 网络voa慢速.py：资源来自网络  

#### 运行结果  
* data.zip：选取VOA某类文章的第一页，共爬取了50条数据

### (2)VOA双语news  
> 数据来源：https://www.51voa.com/Bilingual_News_1.html  

#### 代码文件  
* [wjl]VOAnews.py：根据“可可英语”的爬虫文件修改的，修改的点在于对于网址的提取+对内容的匹配

#### 运行结果   

data.zip：爬取前几页的结果
