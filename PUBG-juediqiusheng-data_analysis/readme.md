## 20G 绝地求生比赛数据集分析

项目主要分析绝地求生72万场比赛的数据，并结合数据给出吃鸡攻略，用数据吃鸡！  
主要的文件为：
- 20G 绝地求生比赛数据集分析.ipynb：Jupyter Notebook格式，代码和说明都在这里
- erangel.jpg：绝地海岛艾伦格地图
- miramar.jpg：热情沙漠米拉玛地图

### 数据集说明：
- 数据主要分成两部分，一部分是玩家比赛的统计数据，在aggregate.zip，一部分是玩家被击杀的数据，在deaths.zip
- 本次分析选取其中的两个数据集进行分析

### 数据集下载链接
- aggregate.zip：https://storage.googleapis.com/kaggle-datasets/9372/13466/aggregate.zip?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1526026719&Signature=LwOY9%2FYOdh%2B%2FGxSmGx7jUR0pHny7gQLGtzOtMB6gsLd9ogS%2BSMYft3XLVAlcLoXRHI487nunH40I3oRSzVfA%2B7S4MbozilVMZO34RNNDrbM0PKUoGDgk9D97btlh0UAI3gtm266kvTWNUQHV%2BJB%2B2CYt5Kzn%2FAF1mBNAVHCgkB%2Bh1DIAy6qbMGKLIirXq5xV2AUePw1oMhmt3NDTBA%2BA%2FZ%2BlTJqNBwXIk50iCzzlvtt2CqLto9rv5nbb%2BWiRK3YlKKKr3WUTIJ%2BX4wbqxJzG4B5njzuJOXq2NYJIX1JXPYGOgFwmKaiqRIrvUhRiUdjJ3EJEC3GZlqF1RA7nXIpd3Q%3D%3D
- deaths.zip：https://storage.googleapis.com/kaggle-datasets/9372/13466/deaths.zip?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1526027703&Signature=iBDH68nWl9xtBk9JEMsQEDXfb2d%2BOR3tDPkjMFakWG%2B7QToAF%2B7mtiGhyhpN6jtR4gQRoKyhTCIqNSNf4gxTawK%2Bd1MVZuOP5KwzO5FFX0Z0x5T8Kt3EvFMYK45dBIV2CJ3bwzQQRuhkPTPkkCvd%2FqPfiFD7n46etCLyvTJjNmWe5GVZL2UM8OEbReE5z72YMPVDGWFQhP%2Bq10uU4BrOAXQrkzNr0MqfCVt8M9vy7Gxp9YsKoGg%2FbK%2FyRGmj2IVadna5vWxReUYqxqxzmNUTndx0H4f6I6looWx1dtF9NB%2B%2BAmyfcuDXCakeGhN9ap2TtcwXbt%2BNzb5Up0foGGO%2Fgg%3D%3D

#### 运行环境：
- python3.6

#### 需要安装的包：
- pandas、numpy、scipy
- matplotlib、seaborn、boke

**注：具体分析说明可以关注微信公众号：Alfred在纽西兰，阅读对应文章**


## PUBG matches data analysis

I analysed over 100 million PUBG matches data and shared some strategies learned from the analysis for playing the game.
The main files are listed below:
- 20G 绝地求生比赛数据集分析.ipynb：The codes and guides are wirrten in this jupyter nootbook file
- erangel.jpg：map of erangel
- miramar.jpg：map of miramar

### Data Statement:
- The data is divided into two parts mainly. One is the statistic data of players in matches, the other is the data of players being killed.
- I chose two datasets for this analysis.

### Datasets download links:
- aggregate.zip：https://storage.googleapis.com/kaggle-datasets/9372/13466/aggregate.zip?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1526026719&Signature=LwOY9%2FYOdh%2B%2FGxSmGx7jUR0pHny7gQLGtzOtMB6gsLd9ogS%2BSMYft3XLVAlcLoXRHI487nunH40I3oRSzVfA%2B7S4MbozilVMZO34RNNDrbM0PKUoGDgk9D97btlh0UAI3gtm266kvTWNUQHV%2BJB%2B2CYt5Kzn%2FAF1mBNAVHCgkB%2Bh1DIAy6qbMGKLIirXq5xV2AUePw1oMhmt3NDTBA%2BA%2FZ%2BlTJqNBwXIk50iCzzlvtt2CqLto9rv5nbb%2BWiRK3YlKKKr3WUTIJ%2BX4wbqxJzG4B5njzuJOXq2NYJIX1JXPYGOgFwmKaiqRIrvUhRiUdjJ3EJEC3GZlqF1RA7nXIpd3Q%3D%3D
- deaths.zip：https://storage.googleapis.com/kaggle-datasets/9372/13466/deaths.zip?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1526027703&Signature=iBDH68nWl9xtBk9JEMsQEDXfb2d%2BOR3tDPkjMFakWG%2B7QToAF%2B7mtiGhyhpN6jtR4gQRoKyhTCIqNSNf4gxTawK%2Bd1MVZuOP5KwzO5FFX0Z0x5T8Kt3EvFMYK45dBIV2CJ3bwzQQRuhkPTPkkCvd%2FqPfiFD7n46etCLyvTJjNmWe5GVZL2UM8OEbReE5z72YMPVDGWFQhP%2Bq10uU4BrOAXQrkzNr0MqfCVt8M9vy7Gxp9YsKoGg%2FbK%2FyRGmj2IVadna5vWxReUYqxqxzmNUTndx0H4f6I6looWx1dtF9NB%2B%2BAmyfcuDXCakeGhN9ap2TtcwXbt%2BNzb5Up0foGGO%2Fgg%3D%3D

#### Python environment
- Python3.6

#### Packages need to be installed
- pandas、numpy、scipy
- matplotlib、seaborn、boke

**Notice: you can find the detailed document by following Alfred's wechat official account: Alfred_Lab**
