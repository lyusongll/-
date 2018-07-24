#!usr/bin/env python
# -*- coding:utf-8 -*-

import re
import requests
import json
import os
import time
#起始url
first_url = "http://tu.duowan.com/m/meinv"

#访问url
r = requests.get(first_url)
r.encoding = 'utf-8'

#取出数据
html = r.text

#取出所有套图id,存入data
data = []
#获取所有li标签
lis = re.findall(r'<li class="box" style="position: absolute;">.*?</li>',html,re.S)
#print(lis)

#获取所有套图id
for li in lis:
	temp = re.findall(r'<a href="http://tu.duowan.com/gallery/(\d+).html" ',li,re.S)[0]
	data.append(temp)
#print(data)

#根据套图id获取图片
url_ = 'http://tu.duowan.com/index.php?r=show/getByGallery/&gid=135353&_=1507966007059'

for gid in data:
	url_ = 'http://tu.duowan.com/index.php?r=show/getByGallery/&gid={}&_={}'.format(gid,int(time.time()*1000))
	

	r2 = requests.get(url_)
	#print(json.loads(r2.text))
	img_dict = json.loads(r2.text)
	#print(img_dict['gallery_title'])

	#创建文件夹 
	os.mkdir(img_dict['gallery_title'])
	#将下载的图片下载到文件夹
	for img in img_dict['picInfo']:
		#下载图片
		img_data = requests.get(img['url']).content  #图片必须保存成content ，文本信息用txt
		print(img['url'])
		#保存到本地
		with open('%s/%s' % (img_dict['gallery_title'],img['title']), 'wb') as f:
			f.write(img_data)



def get_img_ids(url):
	#访问url
	r = requests.get(first_url)
	r.encoding = 'utf-8'

	#取出数据
	html = r.text

	#取出所有套图id,存入data
	data = []
	#获取所有li标签
	lis = re.findall(r'<li class="box" style="position: absolute;">.*?</li>',html,re.S)
	#print(lis)

	#获取所有套图id
	for li in lis:
		temp = re.findall(r'<a href="http://tu.duowan.com/gallery/(\d+).html" ',li,re.S)[0]
		data.append(temp)
	#print(data)
	return data

def get_img_info(img_ids):
	res = []
	for gid in img_ids:
		url_ = 'http://tu.duowan.com/index.php?r=show/getByGallery/&gid={}&_={}'.format(gid,int(time.time()*1000))
	

		r2 = requests.get(url_)
		#print(json.loads(r2.text))
		img_dict = json.loads(r2.text)
		#print(img_dict['gallery_title'])

		res.append(img_dict)

	return res


def get_img(img_dict):
	os.mkdir(img_dict['gallery_title'])
	#将下载的图片下载到文件夹
	for img in img_dict['picInfo']:
		#下载图片
		img_data = requests.get(img['url']).content  #图片必须保存成content ，文本信息用txt
		print(img['url'])
		#保存到本地
		with open('%s/%s' % (img_dict['gallery_title'],img['title']), 'wb') as f:
			f.write(img_data)


def run(first_url):
	#获取套图ids
	img_ids = get_img_isd(url)
	#获取所有套图信息
	img_info = get_img_info(img_ids)

	for img in img_info:
		get_img(img)

if __name__ == '__main__':
	first_url = "http://tu.duowan.com/m/meinv"
	run(first_url)
