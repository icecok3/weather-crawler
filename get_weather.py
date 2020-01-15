'''
@Author: icecok3
@Date: 2019-04-28 
@LastEditTime : 2019-06-25 
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re 
import requests
import json
import time
import sys
from retrying import retry


##json数据包格式
# {'od21': '20', 'od22': '15', 'od23': '328', 'od24': '西北风',
#  'od25': '2', 'od26': '0.0', 'od27': '90', 'od28': ''}
# 
# od21：小时(超过整点按当前整点算，下一整点更新当前整点数据)
# od22：温度
# od24：风向
# od35：风力
# od26：降水量
# od27：湿度

@retry
def get_date(u1,u2,city_name):
    try:
        r = requests.get(url = u1)
        r.encoding = "utf8"
        html = r.text

        ##匹配json数据包
        soup = BeautifulSoup(html,"html.parser")
        #soup = BeautifulSoup(html,"lxml")
        pattern = re.compile(r"var observe24h_data =(.*?);",re.MULTILINE | re.DOTALL)#匹配存放数据数据的json包
        script = soup.find("script", text=pattern)
        j = json.loads(pattern.search(script.text).group(1))['od']['od2']#从json包中获取相应的数据块
        j = j[:-1]#去掉过去第24小时的数据
        #print(j)
        #print(type((json.loads(j)['od']['od2'])))

        temperature = []   #温度
        humidity = []      #湿度
        precipitation = [] #降水
        #wind_speed = []    #风速
        #wind_dir = []      #风力
        temperature_avg = 0
        humidity_avg = 0
        while j[0]['od21'] < "20":
            print("20点信息还未更新，将于10秒后重新获取....")
            time.sleep(10)
            raise Warning("正在重新获取....")

        for i in j:
            if i['od24'] == "无持续风向":
                temperature.append(temperature[-1])       
                humidity.append(humidity[-1])               
                precipitation.append(precipitation[-1])
                #print(type(i['od22']))
            else:
                temperature.append(float(i['od22']))             #过去24小时温度
                humidity.append(float(i['od27']))                #湿度
                precipitation.append(float(i['od26']))           #降水量  
                #wind_speed.append(float(i['od26']))              #风速
                #wind_dir.append(i['od24'])                       #风力
            if i['od21'] in ['02','08','14','20']:
                temperature_avg = temperature_avg + i['od22']
                #print(temperature_avg)
                humidity_avg = humidity_avg + i['od27']
                #print(humidity_avg)


        r2 = requests.get(url = u2)
        r2.encoding = "utf8"
        html2 = r2.text
        soup2 = BeautifulSoup(html2,"html.parser")
        #print(soup2.select(".blue-item active"))
        wind = soup2.find("li",{"class":"blue-item active"}).find("p",{"class":"wind-info"}).string.strip() #获取风力


        #print(temperature_avg/4,humidity_avg/4)
        date = [max(temperature),min(temperature),temperature_avg/4,max(humidity),min(humidity),humidity_avg/4,sum(precipitation),wind]
        #print(date)
        return date
    except BaseException as e:
        print("爬取{}数据异常,异常信息:{}".format(city_name,e))
        print("重试中...")
        time.sleep(3)
        raise Exception(e)



def start():
    with open("city_url.txt","r",encoding = "utf8") as f:
        for line in f:#依此从文件中读取每一行
            if line != None:
                city_name,city_url = (line.split()[0]),(line.split()[1])#这里获取了目标城市的名字和对应网址
                city_url2 = city_url.replace("weather1dn","weathern")
                d = get_date(city_url,city_url2,city_name)
                i = [time.strftime('%Y-%m-%d',time.localtime(time.time())),city_name]
                i.append(d)
                print("{}:".format(city_name),d)
                infor = " ".join(map(str,i))
                save(infor)
                print("{} {}已保存".format(city_name,str(i[0])))
        
        save("\n")



def save(l):
    with open ("information.txt","a",encoding = "utf8") as f:
        f.write(l)
        f.write("\n")


if __name__ == "__main__":
    #u = "http://www.weather.com.cn/weather1d/101210101.shtml"
    #u = "http://forecast.weather.com.cn/town/weather1dn/101120507013.shtml"
    #get_date(u)
    start()

