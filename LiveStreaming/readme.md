## 爬取了西瓜直播的主播直播数据107.5万条，并分析直播平台和游戏主播行业是否真如我们想象般的暴利（北上广深租房图鉴）

项目主要使用多线程爬虫爬取了西瓜直播（今日头条旗下APP）各类型游戏的主播直播数据107.5万条，并分析直播平台和游戏主播行业是否真如我们想象般的暴利


主要的文件为：
- get_live_data.py：多线程爬虫，每隔5分钟爬取一次西瓜直播（今日头条旗下APP）各类型游戏的主播直播数据（需要安装mongodb）
- get_streamer_info.py：根据user_id爬取主播的个人公开信息
- xigua.ipynb: Jupyter notebook代码，对直播数据进行分析
- stopwords.txt: 停用词表

#### 运行环境：
- python3.6

#### 需要安装的包：
- requests
- pyecharts
- pandas
- numpy
- pymongo

**注：具体分析说明可以关注微信公众号：[Alfred数据室](https://wx1.sinaimg.cn/mw690/007yVcwsgy1g03lo67ikoj30u00f0ta0.jpg)，阅读对应文章《[游戏直播行业真的如你想象般暴利？](https://mp.weixin.qq.com/s/-B8cWjB6db6t0gNmqJ34GQ)》**
