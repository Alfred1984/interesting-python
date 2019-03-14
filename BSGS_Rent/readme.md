## 爬取并分析北上广深链家网租房房源全部数据，得出租房建议（北上广深租房图鉴）

项目主要爬取北上广深链家网全部租房房源数据，并且得出租金分布、租房考虑因素等建议

主要的文件为：
- house_data_crawler.py：爬取北上广深租房房源数据的代码（带说明和注释, 需要安装mongodb）
- info.py：租房类型和各城市各区域的信息，供house_data_crawler.py调用
- 北上广深租房图鉴.ipynb: Jupyter notebook代码，对北上广深租房数据进行分析
- data_sample.csv: 租房数据，这里只随机选择了12000条，每城市3000条

#### 运行环境：
- python3.6

#### 需要安装的包：
- requests
- pyecharts
- pandas
- numpy
- pymongo

**注：具体分析说明可以关注微信公众号：[Alfred数据室](https://wx1.sinaimg.cn/mw690/007yVcwsgy1g03lo67ikoj30u00f0ta0.jpg)，阅读对应文章《[北上广深租房图鉴](https://mp.weixin.qq.com/s/sb-g7sGmPJPIsfF23INlmQ)》**


## Crawling and analysing Bei-Shang-Guang-Shen rent data from Lianjia.

This project Crawls Bei-Shang-Guang-Shen renting data from Lianjia, and analyses the distribution of the rent, and provides renting advices in those cities.
The main files are listed below:
- house_data_crawler.py：codes for crawling Bei-Shang-Guang-Shen rent data from Lianjia（with annotation, MongoDB needs to be installed.）
- info.py：infos about renting type and districts of Bei-Shang-Guang-Shen，for house_data_crawler.py
- 北上广深租房图鉴.ipynb: Jupyter notebook codes，analysing Bei-Shang-Guang-Shen renting data
- data_sample.csv: 12000 renting data by random choices

#### Python environment
- Python3.6

#### Packages need to be installed
- requests
- pyecharts
- pandas
- numpy
- pymongo

**Notice: you can find the detailed document by following Alfred's wechat official account: [Alfred_Lab](https://wx1.sinaimg.cn/mw690/007yVcwsgy1g03lo67ikoj30u00f0ta0.jpg)**
