# weather-crawler
一个简单的天气爬虫


* 运行get_weather.py能获取结果，输出格式为:

        (城市名):[最大温度，最小温度，平均温度，最大湿度，最小湿度，平均湿度，总降水量]  
        
* 所爬取内容为过去23小时的数据，程序执行条件的为判断中国天气网是否更新21点的数据（计算平均值时使用了21点的数据，且平均温度只用了四个时段的温度进行计算）


* 如果爬取结果报错的话，可能是因为当前网络质量或者中国天气网服务器的问题，可以稍后重新运行一下


* 如果想要添加新的地区，请在city_url中以以下格式添加新的一行（看一下txt中的内容就能明白）：

        城市名字（空格）对应网址

