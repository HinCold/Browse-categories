# Browse-categories
Base on machine learning to analysis what kind of scene I am browse with vision. key word: opencv, SDT, OCR, TextClassification
# 数据集

## 爬虫

### 代码结构

├─data
│  ├─0
│  ├─1
│  ├─2
│  ├─3
│  ├─4
│  ├─5
│  ├─6
│  ├─7
│  ├─8
│  └─9
└─dataSet
   ├─multiPro.py
   └─utils.py

数据被预先分为十个类别，依据类别通过百度搜索爬取相关内容。后期在细分。

### utils.py

作为爬虫工具集：主要是解析页面源码连接和更新带爬队列和去重集合，还涉及初始化浏览器和浏览器请求页面及弹窗处理

### multiPro.py

为爬虫工作开启多进程支持。主进程开启两个子进程，共享Process管理下的带爬队列实现进程通信和同步。

主要步骤：加载资源集合，搜索相关内容，启动工作进程
# contiuning...
