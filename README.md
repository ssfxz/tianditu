# 国家统计局地图数据源-天地图数据爬虫


## 天地图js4.0的API示例获得数据搜索接口

http://lbs.tianditu.com/api/js4.0/examples.html

引擎接口工具 -> 搜素 -> 根据关键词本地搜素

## 天地图地图数据接口
http://api.tianditu.com/search?postStr={"keyWord":"北京","level":"1","mapBound":"60,0,150,60","queryType":"1","start":"0","count":"10"}


## 国家统计局发布的行政区目录

http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/

整理为china.txt

## getCity.py
将china.txt中的行政区格式化后按照省市区级划分到

* province.txt
* city.txt
* county.txt

## fetchData.py
根据行政区列表爬取地图数据
useage：> fetchData.py province.txt

生成对应的目录以及聚合后的collect.js文件

## drawmap.html
根据聚合后的collect.js数据绘制地图用以检验
抓取的数据