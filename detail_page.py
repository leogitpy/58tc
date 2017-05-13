# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from bs4 import BeautifulSoup
import requests
import re
#import db
import down_img
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.58.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}

def get_soup(url):
    wb_data = requests.get(url,headers = headers)
    soup = BeautifulSoup(wb_data.text,'lxml')
    return soup

def get_floor(content):
    floor = re.findall(r'类型：(.+?)层；装修',content)[0]
    return floor

def get_img(url):
    print(url)
    soup = get_soup(url)
    house_img = soup.select('#generalType > div > ul > li > img')   #房子照片
    i = 0
    for img in house_img:
        #下载不超过10张图片
        if i<10:            
            img = re.findall(r'src="(.+?)\?w=',str(img))
            if img:                
                img_url = img[0]
                down_img.download_img(url,img_url)
                print('来自' + img_url)
        else:
            break
        i+=1
        
    
def get_detail_info(url):   
    wb_data = requests.get(url,headers = headers)
    soup = BeautifulSoup(wb_data.text,'lxml')    
    #详细页标题
    title = soup.title.text  
#    print(title)
    post_time = soup.find_all('span', attrs={'class':'up'})[0].text  #提交时间  
    visit_count = soup.find_all('span', attrs={'class':'up'})[1].text  #访问人数    
    village = soup.find_all('span',attrs={'class':'c_000 mr_10'})[0].text  #小区
    village = village.replace('\n','')
    village = village.replace('\r','')
    village = village.replace(' ','')
    area = soup.find_all('span',attrs={'class':'main'})[1].text  #面积
    floor = get_floor(soup.find('meta',attrs={'name':'description'})['content'])    #楼层
    room_structure = soup.find_all('span',attrs={'class':'main'})[0].text    #几室几厅
    decoration = soup.find_all('span',attrs={'class':'sub'})[1].text     #装修
    poster = soup.find_all('span',attrs={'class':'f14 c_333 jjrsay'})[0].text   #发布人
    poster_desc = soup.find_all('p',attrs={'class':'c_999 lh22 jjr-desc'})[0].text  #发布人描述
    poster_phone = soup.find_all('p',attrs={'class':'phone-num'})[0].text   #联系电话
    price = soup.find_all('span',attrs={'class':'price'})[0].text    #总价
    unit = soup.find_all('span',attrs={'class':'unit'})[0].text    #总价
    unit = unit.replace(' ','')
    urlstr = re.findall('ershoufang/(.+?)\.shtml',url)[0]
#    house_img = soup.select('#generalType > div > ul > li > img')   #房子照片   
#    print(village) 
    return url,title,post_time,visit_count,village,area,floor,room_structure,decoration,poster,poster_desc,poster_phone,price,unit,urlstr
#detail_url = 'http://pe.58.com/ershoufang/27678620068284x.shtml'
##detail_url = 'http://pe.58.com/ershoufang/29937806458952x.shtml'
#
#
#wb_data = requests.get(detail_url,headers = headers)
#soup = BeautifulSoup(wb_data.text,'lxml')
#
#title = soup.title.text
##louceng = soup.find('meta',attrs={'name':'description'})['content']
#
#print(title)
#
#poster = soup.find_all('span',attrs={'class':'f14 c_333 jjrsay'})
#poster_desc = soup.find_all('p',attrs={'class':'c_999 lh22 jjr-desc'})
#poster_phone = soup.find_all('p',attrs={'class':'phone-num'})
#up_time = soup.find_all('span', attrs={'class':'up'})  #提交时间
#house_img = soup.select('#generalType > div > ul > li > img')
#print(poster[0].text)
#print(poster_desc[0].text)
#print(poster_phone[0].text)
#print(up_time[0].text)
#print(up_time[1].text)
##for img in house_img:
##    src_img = re.findall(r'(.+?)\?w=',img.get('data-src'))[0]
##    print(src_img)
#
#line = '出售曙光小区2楼住房,送露台10㎡,单位住房,无管理费;售价：48万元（5052元/㎡）；房贷：首付约14.4万月供约（1376元）；产权：商品房2000年建；类型：普通住宅  2/6层；装修：中等装修朝南北；'
#
#print(re.findall(r';售价：(.*)\；房贷：',line)[0])
#louceng = re.findall(r'(...)层；装修',line)[0]
#print(louceng)
#zhuangxiu = re.findall(r'装修：(.+?)\；',line)[0]
#print(zhuangxiu)