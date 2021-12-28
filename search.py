
import numpy as np
import pandas as pd
import requests
import json
import sys
import time

def search_poi(index,x1,y1,x2,y2,divt,poi_type,page):
	global keyi
	global api_count
	#构建URL
	x1 = float(x1)
	y1 = float(y1)
	x2 = float(x2)
	y2 = float(y2)
	polygon = str(x1)+','+str(y1)+'|'+str(float(x2))+','+str(float(y2))
	u= "https://restapi.amap.com/v3/place/polygon?key="+keys[keyi]+'&polygon='+polygon +'&types='+poi_type+'&extensions=all&output=json&offset=25&page='+str(page)
	api_count += 1 #记录一次调用

	#单个key超出2000次限额，更换key
	if api_count>=2000:
		keyi += 1
		print("change key!now key is",keys[keyi])
		api_count=0

	#解析数据
	data=requests.get(u)
	s=data.json()
	#查询错误
	if s['status']!='1':
		print('eror!')
		return

	#如果网格太大，递归查询
	
	if int(s['count'])>950:

		print("too much!count is"+s['count'],s['pois'])
		# search_poi(index,x1,y1,x2,y2,divt/2,poi_type,1)
    
		# search_poi(index,x1,y1,x+divt/2,y,divt/2,poi_type,1)
		# search_poi(index,x,y+divt/2,divt/2,poi_type,1)
		# search_poi(index,x+divt/2,y+divt/2,divt/2,poi_type,1)
		return

	#这里可以按照需求，修改成存储结果，我这里只做了输出
	# print('now location:',x,y,divt,';now page:',page,'now api count:',api_count)
	
	if len(s['pois'])>0:
		f = open("./test.txt","a+",encoding='utf_8_sig')
		for i in range(len(s['pois'])):
			f.write(str(index)+','+str(s['pois'][i]['name'])+','+str(s['pois'][i]['typecode'])+','+str(s['pois'][i].get('address',None))+','+str(s['pois'][i].get('location',None))+','+str(s['pois'][i].get('tel',None))+','+str(s['pois'][i]['biz_ext'].get('rating',None))+','+str(s['pois'][i]['biz_ext']['cost'])+'\n')
				
		time.sleep(0.5)	
	#若不止一页，查询下一页
	if len(s['pois'])==25:
		search_poi(index,x1,y1,x2,y2,divt,poi_type,page+1)
	
#main	
keys = ['c352b674499cf76fb4f7e00577cc46db','8dca971e5198373566d90726079ad0b0','','D','E','F','G','H','I','J']	#自己申请的10个key
global keyi						#当前使用的key编号
global api_count					#每一个key调用api的次数
keyi = 0
api_count=0
div = 0.1 						#设置网格大小
poi_type='050000'					#当前搜索的POI类，具体参考
grid_jw = pd.read_csv('./grid.csv',header=None)   #保存的上海网格数据

#对所有网格循环搜索POI
for index,rows in grid_jw[1:].iterrows():				
	search_poi(index,rows[1],rows[2],rows[3],rows[4],div,poi_type,1)
