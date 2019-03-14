## 随机抓取蔡徐坤100万+转发的微博的转发数据，并且分析其真假流量的比例（用大数据扒一扒蔡徐坤的真假流量粉）

项目主要随机抓取蔡徐坤100万+转发的微博《再见，“任性的”千千…》的10万条转发数据，并且分析蔡徐坤真假转发流量的比例以及真假粉丝的用户画像

主要的文件为：
- CaiXuKun: 爬取转发数据的Scrapy爬虫代码（带说明和注释, 需要安装mongodb以及Scrapy）
- scrapy.cfg: Scrapy配置文件
- CaiXuKun.ipynb: Jupyter notebook代码，对转发数据进行分析
- stopwords.txt: 停用词表

#### 数据
蔡徐坤一条100万+微博下的102313条转发数据
- 下载链接：https://pan.baidu.com/s/1wykRx5gMZhgD8rQG78wf9A

#### 运行环境：
- python3.6

#### 需要安装的包：
- requests
- pyecharts
- pandas
- numpy
- pymongo
- scrapy

**注：具体分析说明可以关注微信公众号：[Alfred数据室](https://wx1.sinaimg.cn/mw690/007yVcwsgy1g03lo67ikoj30u00f0ta0.jpg)，阅读对应文章《[用大数据扒一扒蔡徐坤的真假流量粉](https://mp.weixin.qq.com/s/j1kgf2RR7jssbWa7uWC-uA)》**


## Randomly crawling and analysing CaiXuKun Weibo repost data.

This project Crawls 100,000+ CaiXuKun Weibo repost data, and analyses the ratio of real and fake reposts.
The main files are listed below:
- CaiXuKun: Scrapy project file for crawling repost data.（with annotation, MongoDB and Scrapy needs to be installed.）
- scrapy.cfg: Scrapy configure file
- CaiXuKun.ipynb: Jupyter notebook codes for analysing the data
- stopwords.txt: stop words list


#### Data
102313 repost data from one of CaiXuKun's Weibo
- download：https://pan.baidu.com/s/1wykRx5gMZhgD8rQG78wf9A

#### Python environment
- Python3.6

#### Packages need to be installed
- requests
- pyecharts
- pandas
- numpy
- pymongo
- scrapy

**Notice: you can find the detailed document by following Alfred's wechat official account: [Alfred_Lab](https://wx1.sinaimg.cn/mw690/007yVcwsgy1g03lo67ikoj30u00f0ta0.jpg)**
