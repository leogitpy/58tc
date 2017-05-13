# -*- coding: utf-8 -*-
"""
Created on Fri May  5 08:49:34 2017
58同城二手房，主程序入口
@author: Leo51888
"""
from bs4 import BeautifulSoup
import requests
import re
import time
import random
import db
import detail_page
#import pymysql
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.58.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}

#headers = {
#        'Accept':'image/webp,image/*,*/*;q=0.8',
#        'Accept-Encoding':'gzip, deflate, sdch',
#        'Accept-Language':'zh-CN,zh;q=0.8',
#        'Connection':'keep-alive',
#        'Cookie':'id58=c5/ns1kV42AZJGKVBLCnAg==; als=0; ipcity=km%7C%u6606%u660E%7C0; city=pe; 58tj_uuid=eecfc2f7-100a-43c9-a0b9-31b52f5bb44c; new_session=0; new_uv=1; utm_source=; spm=; init_refer=; commontopbar_city=9444%7C%u666E%u6D31%7Cpe; firstLogin=true; commonTopbar_myfeet_tooltip=end',
#        'Host':'tracklog.58.com',
#        'Referer':'http://pe.58.com/?PGTID=0d000000-0000-091e-f115-181fc16cc05a&ClickID=1',
#        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
#}


url = 'http://pe.58.com/ershoufang/pn1/'

#列表页抓取详细页URL
#def list_get_detail:     
wb_data = requests.get(url,headers = headers)
soup = BeautifulSoup(wb_data.text,'lxml')

#print(soup.find(class_='no-result'))
#判断是否有房源信息 class="no-result"
i = 29
#如果遇到无房源则停止
while not soup.find(class_='no-result'):
#while i==1:
    
    url = 'http://pe.58.com/ershoufang/pn' + str(i) +'/'
    print(url)
    wb_data = requests.get(url,headers = headers)
    soup = BeautifulSoup(wb_data.text,'lxml')
    all_url = soup.select('a.t')
#    print(all_url)


       
    for tmp_url in all_url:
        #取列表页中精华项房源地址
        if re.findall(r'^http://jxjump.+?entinfo=(.+?)_0',tmp_url['href']):
            jxjump = re.findall(r'^http://jxjump.+?entinfo=(.+?)_0',tmp_url['href'])
            jxjump = 'http://pe.58.com/ershoufang/' + jxjump[0] + 'x.shtml'
            urlstr = re.findall('ershoufang/(.+?)\.shtml',jxjump)[0]
#            print(urlstr)
#            print(db.if_exist_urlstr(urlstr))
            #判断数据库中是否已经存在
            if not db.if_exist_urlstr(urlstr):
                #写入数据表detail_url                
#                db.insert_detail_url(jxjump)
                #取精华详细信息
                detail_info = detail_page.get_detail_info(jxjump)
                db.insert_detial_info(detail_info)

        #取列表页中置顶项房源地址
        if re.findall(r'^http://short.+?entinfo=(.+?)_0',tmp_url['href']):
            short = re.findall(r'^http://short.+?entinfo=(.+?)_0',tmp_url['href'])
            short = 'http://pe.58.com/ershoufang/' + short[0] + 'x.shtml'
            urlstr = re.findall('ershoufang/(.+?)\.shtml',short)[0]
#            print(urlstr)
#            print(db.if_exist_urlstr(urlstr))
            #判断数据库中是否已经存在
            if not db.if_exist_urlstr(urlstr):
#                db.insert_detail_url(short)
                #取置顶详细信息
                detail_info = detail_page.get_detail_info(short)
#               print(detail_info)
                db.insert_detial_info(detail_info)
                #获取详细页图片，下载，并存入数据库
#               detail_page.get_img(short)
            

        #取列表页中每项（除了精华、置顶格式不一样）房源地址
        if re.findall(r'(.+?)\?psid=',tmp_url['href']):           
            normal = re.findall(r'(.+?)\?psid=',tmp_url['href'])[0]   
            urlstr = re.findall('ershoufang/(.+?)\.shtml',normal)[0]
#            print(urlstr)
#            print(db.if_exist_urlstr(urlstr))
            #判断数据库中是否已经存在
            if not db.if_exist_urlstr(urlstr):
#                db.insert_detail_url(normal)
#               print(normal_list)
                #取普通详细信息
                detail_info = detail_page.get_detail_info(normal)
                db.insert_detial_info(detail_info)
#        time.sleep(random.randint(3,5))
#        print(tmp_url)
    i += 1
    time.sleep(random.randint(5,15))
    #all_url = soup.select('a[href^="http://pe.58.com/ershoufang/"]')
    #print(soup)
    #print(all_url)