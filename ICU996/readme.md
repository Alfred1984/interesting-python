## 爬取Github热门项目996.ICU中Issues页面的10037条讨论数据和39987条点了star的程序员Github个人信息数据，并且分析这群抵制996的程序员都是何方神圣（大胆，都是哪些程序员在反对996？！）

项目主要通过Github API爬取Github热门项目996.ICU中Issues页面的10037条讨论数据和39987条点了star的程序员Github个人信息数据，并且用这些数据对抵制996的程序员进行画像

主要的文件结构为：
```
├── ICU996                  Scrapy爬虫项目
│   ├── ICU996
│   │   ├── __init__.py
│   │   ├── items.py        items文件
│   │   ├── middlewares.py  中间件文件
│   │   ├── pipelines.py    管道文件
│   │   ├── settings.py     设置文件
│   │   ├── spiders         
│   │   │   ├── __init__.py
│   │   │   └── a996.py     爬虫文件
│   │   └── stargazers.csv  点了star的程序员简要数据，主要从这里提取个人简介页面的url，从数据下载处下载
│  └── scrapy.cfg
└── analysis                数据分析
    ├── 996.ipynb           Jupyter notebook代码
    ├── stopwords.txt       停用此表，用于绘制词云图
    ├── issues_data.csv     爬取回来的issues数据，从数据下载处下载
    └── users_data.csv      爬取回来的users数据，从数据下载处下载
```

#### 数据下载
- stargazers.csv：https://pan.baidu.com/s/1K9BX36TnarbJ5tVELGKejw
- issues_data.csv/users_data.csv：https://pan.baidu.com/s/1iwcXRx2jB5BretOrHb5iCQ

#### 注意的问题：
- 由于该项目做得比较快，爬虫都是在测试中就把数据爬回来了，所以项目代码比较不规整；
- 数据是通过Github API爬取的（不得不说，这个API是我用过的最好用的API），需要先申请Personal access tokens（不然每小时单个IP只能请求60次，有token的话，每20分钟可以请求5000次）
- Personal access tokens申请方法：打开Github——`Settings`——`Developer settings`——`Personal access tokens`——`Generate new token`，自行申请就好，记得把read:user这一项勾上，因为后面我们要请求user的个人公开信息
- 我的爬取顺序是先爬Issues数据，再爬stargazers简要数据，再从中提取了url，进而爬取每个stargazers的个人公开简介数据，当然你也可以改写一下代码，每爬回一页stargazers简要数据，从中提取url，直接请求每个stargazers的个人公开简介数据

#### Github API

项目中的爬虫仅仅是爬取Github个人公开信息的，其它的API如下：

##### [Issues](https://github.com/996icu/996.ICU/issues): 

https://api.github.com/repos/996icu/996.ICU/issues?page=()&access_token=(), 其中page（页面）参数和access_token参数（你申请回来的token）需自行传递
```
# start_requests可以这样写

def start_requests(self):
        urls = ['https://api.github.com/repos/996icu/996.ICU/issues?page={}&access_token=xxx'.format(i) for i in range(1, 400)]
        random.shuffle(urls)  # 这里爬400页issues数据，random shuffle一下可以保证爬的数据更全一些

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
```

##### [Stargazers](https://github.com/996icu/996.ICU/stargazers)：

https://api.github.com/repos/996icu/996.ICU/stargazers?page=()&access_token=(), 其中page（页面）参数和access_token参数（你申请回来的token）需自行传递
```
# start_requests可以这样写
def start_requests(self):
        urls = ['https://api.github.com/repos/996icu/996.ICU/stargazers?page={}&access_token='.format(i) for i in range(1, 2239)]
        random.shuffle(urls)  # 这里爬2239页stargazers数据，当然现在已经不止那么多页了，random shuffle一下可以保证爬的数据更全一些

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
```

#### 运行环境：
- python3.6

#### 需要安装的包：
- requests
- pyecharts
- pandas
- numpy
- pymongo
- scrapy

**注：具体分析说明可以关注微信公众号：[Alfred数据室](https://wx1.sinaimg.cn/mw690/007yVcwsgy1g03lo67ikoj30u00f0ta0.jpg)，阅读对应文章《[大胆，都是哪些程序员在反对996？！](https://mp.weixin.qq.com/s/BZhHcEwdUJNJRVFix8NRSQ)》**
