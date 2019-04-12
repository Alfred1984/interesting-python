## 爬取英语外籍老师与本土老师招聘数据（没经验没学历的外教为啥能拿1.4W+的高薪？）

项目主要爬取外籍人员招聘网站JobLEADChina上的外籍英语老师招聘数据945条，万行教师人才网上的英语老师招聘数据5780条，以及微信群成员信息498条，并分析外教教师的招聘状况


主要的文件为：
- jobleadchina.py：爬取外籍人员招聘网站JobLEADChina上的外籍英语老师招聘数据代码
- local_english_teacher.py：爬取万行教师人才网上的英语老师招聘数据代码
- wechat_group_member.py：爬取微信群成员信息代码
- 数据分析.ipynb：Jupyter notebook代码，对外教教师的招聘状况进行分析

#### 数据
- **JobLEADChina数据**：jobleadchina.csv
- **万行教师人才网招聘数据**：幼儿园.csv，中小学.csv，职业院校.csv，外语培训.csv
- **微信群成员数据**：data_gm.csv

#### 运行环境：
- python3.6

#### 需要安装的包：
- requests
- pyecharts
- pandas
- numpy

**注：具体分析说明可以关注微信公众号：[Alfred数据室](https://wx1.sinaimg.cn/mw690/007yVcwsgy1g03lo67ikoj30u00f0ta0.jpg)，阅读对应文章《[没经验没学历的外教为啥能拿1.4W+的高薪？](https://mp.weixin.qq.com/s/BMfiB08gWy66zzvCe2lJmQ)》**
