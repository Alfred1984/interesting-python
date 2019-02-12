## 爬取和分析电影《流浪地球》的猫眼评论（十万条评论告诉你，给《流浪地球》评1星的都是什么心态？）

项目主要爬取电影《流浪地球》的猫眼评论，把评论保存到mongodb，并且分析该电影出现低分的原因

主要的文件为：
- comment_crawler.py：爬取电影《流浪地球》的猫眼评论的代码（带说明和注释，需要安装MongoDB数据库）
- TheWanderingEarth.ipynb：Jupyter notebook代码，分析该电影的评论和评分
- data.csv: 从MongoDB提取出来的10万条数据

#### 运行环境：
- python3.6
- 本地MongoDB数据库

#### 需要安装的包：
- requests
- pymongo
- pyecharts
- pandas
- numpy
- jieba

**注：具体分析说明可以关注微信公众号：[Alfred数据室](https://mmbiz.qpic.cn/mmbiz_png/deBiaBx31sgsbOMcxxmJkmQJmtq7ticTPR3trcMG4OFUy9atYBiaFCt4icRa5Tich9w1GNxYLaCuPFlpl6b88DpH2PA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)，阅读对应文章《[十万条评论告诉你，给<流浪地球>评1星的都是什么心态？](https://mp.weixin.qq.com/s/3d_ycK0D1KfbjQJ3m7FhEQ)》**


## Crawling and analysing MaoYan comments of The Wandering Earth

This project Crawls MaoYan comments of The Wandering Earth, and saves the comments data into MongoDB. It reveals the reason why the movie is getting some bad reputation.
The main files are listed below:
- comment_crawler.py：codes for crawling MaoYan comments of The Wandering Earth(with annotation, MOngoDB
needs to be installed.)
- TheWanderingEarth.ipynb：Jupyter notebook for analysing the comments and scores
- data.csv: 100000+ comment data extracted from MongoDB.

#### Python environment
- Python3.6
- MongoDB

#### Packages need to be installed
- requests
- pymongo
- pyecharts
- pandas
- numpy
- jieba

**Notice: you can find the detailed document by following Alfred's wechat official account: [Alfred_Lab](https://mmbiz.qpic.cn/mmbiz_png/deBiaBx31sgsbOMcxxmJkmQJmtq7ticTPR3trcMG4OFUy9atYBiaFCt4icRa5Tich9w1GNxYLaCuPFlpl6b88DpH2PA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)**
