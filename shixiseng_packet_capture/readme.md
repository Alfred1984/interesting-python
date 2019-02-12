## 换种姿势爬取“实习僧”网站之手机抓包

项目很简单，主要过程在与手机抓包分析和获取iso端的数据接口，有了接口便可以直接编写代码爬取数据。
主要的文件为：
- sxs_app.py：通过iso端爬取实习僧网站的代码
- job_list.csv，job_detailed.csv，com_detailed.csv：爬取回来的“数据挖掘”关键字下的职位列表数据、职位详情数据和公司主业数据

#### 运行环境：
- Python3.6

#### 需要安装的包：
- pandas
- requests

**注：具体分析说明可以关注微信公众号：[Alfred数据室](https://wx1.sinaimg.cn/mw690/007yVcwsgy1g03lo67ikoj30u00f0ta0.jpg)，阅读对应文章《[回复“实习僧”CTO之换种姿势爬取实习僧网站](https://mp.weixin.qq.com/s/UF3SF_cpbx8PFkva7rWW3Q)》**

## Another approach for "shixiseng.com" crawling

Easy project. The main tackle is finding out iso data api by phone packet capturing. Once found out, code wrriting is an easy work.
Main files are listed below:
- sxs_app.py：Python codes for crawling "shixiseng.com" by ios data api
- job_list.csv，job_detailed.csv，com_detailed.csv：the data crawled from "shixiseng.com" by the keyword "数据挖掘"（data mining）

#### Python environment
- Python3.6

#### Packages need to be installed
- pandas
- requests

**Notice: you can find the detailed document by following Alfred's wechat official account: [Alfred_Lab](https://wx1.sinaimg.cn/mw690/007yVcwsgy1g03lo67ikoj30u00f0ta0.jpg)**
