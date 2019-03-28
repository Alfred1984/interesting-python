## 爬取丁香人才网的医生招聘数据，并且分析儿科医生的生存处境（儿科医生的眼泪，全被数据看见了）

项目主要爬取丁香人才网10950条涵盖儿科、内科、外科、妇产科、眼科的招聘数据，并且分析儿科医生的真实处境

主要的文件为：
- dingxiang_job.py: 爬取招聘数据的爬虫代码（带说明和注释，需要自行配置代理IP，需要安装MongoDB）
- 儿科医生.ipynb: Jupyter notebook代码，对儿科医生招聘数据进行分析
- all_data.csv: 10950条招聘数据

#### 运行环境：
- python3.6

#### 需要安装的包：
- requests
- pyecharts
- pandas
- numpy
- pymongo

#### 需要注意的问题：
- API：通过丁香人才网在微信小程序上的API进行爬取的（需要抓包分析）
- 爬取方法：先按照省份，再按照单位类型（因为直接按照省份抓，返回的数据有限）
- 反反爬虫：丁香人才网反爬虫的措施是限制IP的请求次数，所以单一IP的话，很快就会被封，必须配置代理IP
- 去重：返回的数据有一些是重复的（特别是不按省份爬，更加细化到按城市爬，返回的数据很多是重复的），所以代码中使用了两套去重小方案：一套是请求前去重，如果Job ID已经请求过了，记录下来，下次就直接不请求了；一套是数据库主键去重。如果按照城市爬的话，建议使用第一套方案。


**注：具体分析说明可以关注微信公众号：[Alfred数据室](https://wx1.sinaimg.cn/mw690/007yVcwsgy1g03lo67ikoj30u00f0ta0.jpg)，阅读对应文章《[儿科医生的眼泪，全被数据看见了](https://mp.weixin.qq.com/s/3SCI4kL-YX-9q1WDY23J-A)》**


## Crawling and analysing Paediatrician recruitment data from DingXiangRenCai.

This project Crawls 10950 recruitment data from DingXiangRenCai, and analyses the situation Paediatrician is facing.
The main files are listed below:
- dingxiang_job.py: codes for crawling recruitment data.（with annotation. Proxies are needed. MongoDB needs to be installed.）
- 儿科医生.ipynb: Jupyter notebook codes for analysing the data
- all_data.csv: 10950 recruitment data


#### Python environment
- Python3.6

#### Packages need to be installed
- requests
- pyecharts
- pandas
- numpy
- pymongo

**Notice: you can find the detailed document by following Alfred's wechat official account: [Alfred_Lab](https://wx1.sinaimg.cn/mw690/007yVcwsgy1g03lo67ikoj30u00f0ta0.jpg)**
