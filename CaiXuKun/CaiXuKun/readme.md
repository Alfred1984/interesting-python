## Scarpy爬虫项目文件

### 项目结构
```
├── CaiXuKUN
│   ├── __init__.py         # 初始文件
│   ├── items.py            # 项目项定义文件
│   ├── middlewares.py      # 项目中间件文件
│   ├── pipelines.py        # 项目管道文件
│   ├── settings.py         # 项目设置文件
│   └── spiders             # 爬虫
│       ├── __init__.py     # 爬虫初始文件
│       └── caixukun.py     # 爬虫文件
└── scrapy.cfg              # 部署配置文件
```

### 需要注意的问题
#### 1. 爬虫名
- caixukun

</br>

#### 2. 启动爬虫
- 切换进Scarpy爬虫项目文件目录，命令行输入 ```scrapy crawl caixukun```

</br>

#### 3. 浏览器抓包
- 爬取的链接：https://m.weibo.cn/api/statuses/repostTimeline?id=4347741368557605&page=1 ，是通过浏览器抓包得来（微博移动端）
- `4347741368557605`是每条微博对应的id，只要通过抓包得到这个id，便可以爬取你想要爬取的任何微博的转发数据
- `page的最大参数`随转发量不同而变化，需要自行测试

</br>

#### 4. 微博反爬的应对措施

直接大批量抓取，很快会被微博反爬，很多page抓取不到数据，应对措施有：

- 在middlewares.py里面增加IP代理
- 在settings.py里面设置爬取间隔时间
- 由于我的代理IP质量不高，所以没有配置代理IP，而是在middlewares.py里增加了一个重试类`TooManyRequestsRetryMiddleware`，只要返回418状态码，整个爬虫暂停1分钟，并在setting.py里面设置了重试次数，当然如果你的代理IP质量好的话，可以直接上代理
