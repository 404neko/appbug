# -*- coding: UTF-8 -*-

import urllib2, re, time, random
from bs4 import BeautifulSoup
import json
import requests
import sys,os
import gzip
from _Config import *

def GetList_360(KeyWord,Number=50):
	def NameUtil():
		pass
	Url_0='http://182.118.31.51/api/search/app?q='
	Url_2='&src=ms_zhushou&page='
	Page=0
	Flag_End=0
	Magnification=1
	Count=1
	List=[]
	while Flag_End==0:
	#if True:
		Url=Url_0+KeyWord+Url_2+str(Page)
		Result=requests.get(Url,headers=Headers).content
		Result=json.loads(Result)
		Json_items=Result['data']
		if len(Json_items)==0:
			Flag_End=1
			continue
		else:
			pass
		for Item in Json_items:
			Title=Item['name']
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

def Get360(KeyWord,AppName):
	def NameUtil():
		pass
	StoreName=u'360 手机助手'
	Key='360'
	Url_0='http://182.118.31.51/api/search/app?q='
	Url_2='&src=ms_zhushou&page='
	Page=0
	Flag_End=0
	Magnification=1
	Count=1
	while Flag_End==0:
	#if True:
		Url=Url_0+KeyWord+Url_2+str(Page)
		Result=requests.get(Url,headers=Headers).content
		Result=json.loads(Result)
		Json_items=Result['data']
		if len(Json_items)==0:
			Flag_End=1
			continue
		else:
			pass
		for Item in Json_items:
			Title=Item['name']
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
