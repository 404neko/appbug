# -*- coding: UTF-8 -*-

import urllib2, re, time, random
from bs4 import BeautifulSoup
import json
import requests
import sys,os
import gzip
from _Config import *

def GetHiapk(KeyWord,AppName):
	Url_0='http://m.baidu.com/s?&tn=native&ver=16785373&platform_version_id=18&st=10a001&word='
	Url_2='&pn='
	StoreName=u'安卓市场'
	Page=0
	Key='hiapk'
	Magnification=1
	Flag_End=0
	Count=1
	while Flag_End==0:
	#if True:
		Url=Url_0+KeyWord+Url_2+str(Page*Magnification)
		Result=requests.get(Url,headers=Headers).content
		Result=json.loads(Result)
		Json_items=Result['result']['data']
		if len(Json_items)==0:
			Flag_End=1
			continue
		else:
			pass
		for Item in Json_items:
			Title=Item['itemdata']['sname']
			#print Title
 			if Title==AppName:
				return {'Store':StoreName,'Rank':str(Count),'Key':Key,'KeyWord':KeyWord}
			else:
				Count+=1
				continue
		if Count>MAX_LOAD:
			Flag_End=1
		else:
			pass
		Page+=1
	return {'Store':StoreName,'Rank':None,'Key':Key,'KeyWord':KeyWord}

def GetList_Hiapk(KeyWord,Number=50):
	Url_0='http://m.baidu.com/s?&tn=native&ver=16785373&platform_version_id=18&st=10a001&word='
	Url_2='&pn='
	Page=0
	Magnification=1
	Flag_End=0
	Count=1
	List=[]
	while Flag_End==0:
	#if True:
		Url=Url_0+KeyWord+Url_2+str(Page*Magnification)
		Result=requests.get(Url,headers=Headers).content
		Result=json.loads(Result)
		Json_items=Result['result']['data']
		if len(Json_items)==0:
			Flag_End=1
			continue
		else:
			pass
		for Item in Json_items:
			Title=Item['itemdata']['sname']
			#print Title
 			if Count>=Number:
				return json.dumps(List)
			else:
				Count+=1
				List.append(Title)
				continue
		if Count>MAX_LOAD:
			Flag_End=1
		else:
			pass
		Page+=1
	return json.dumps(List)
