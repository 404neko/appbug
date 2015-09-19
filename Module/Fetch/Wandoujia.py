# -*- coding: UTF-8 -*-

import urllib2, re, time, random
from bs4 import BeautifulSoup
import json
import requests
import sys,os
import gzip
from _Config import *

def GetWandoujia(KeyWord,AppName):
	#http://ias.wandoujia.com/api/v2/search?&type=APPS&mode=VERTICAL&id=wandoujia_android&start=40&q=%E6%B5%8F%E8%A7%88%E5%99%A8&ch=wandoujia_web
	StoreName=u'豌豆荚'
	Magnification=10
	Key='wandoujia'
	Url_0='http://ias.wandoujia.com/api/v2/search?&type=APPS&mode=VERTICAL&id=wandoujia_android&start='
	Url_2='&q='
	Url_4='&ch=wandoujia_web'
	Page=0
	Flag_End=0
	Count=1
	while Flag_End==0:
	#if True:
		Url=Url_0+str(Page*Magnification)+Url_2+KeyWord+Url_4
		Result=requests.get(Url,headers=Headers).content
		Result=json.loads(Result)
		try:
			Json_items=Result['sections'][0]['items']
		except:
			Flag_End=1
		if len(Json_items)==0:
			Flag_End=1
			break
		else:
			pass
		for Item in Json_items:
			Title=Item['content']['title'].replace('<em>','').replace('</em>','')
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

def GetList_Wandoujia(KeyWord,Number=50):
	#http://ias.wandoujia.com/api/v2/search?&type=APPS&mode=VERTICAL&id=wandoujia_android&start=40&q=%E6%B5%8F%E8%A7%88%E5%99%A8&ch=wandoujia_web
	Magnification=10
	Url_0='http://ias.wandoujia.com/api/v2/search?&type=APPS&mode=VERTICAL&id=wandoujia_android&start='
	Url_2='&q='
	Url_4='&ch=wandoujia_web'
	Page=0
	Flag_End=0
	Count=1
	List=[]
	while Flag_End==0:
	#if True:
		Url=Url_0+str(Page*Magnification)+Url_2+KeyWord+Url_4
		Result=requests.get(Url,headers=Headers).content
		Result=json.loads(Result)
		Json_items=Result['sections'][0]['items']
		if len(Json_items)==0:
			Flag_End=1
			break
		else:
			pass
		for Item in Json_items:
			Title=Item['content']['title'].replace('<em>','').replace('</em>','')
			#print Title
 			if Count>=Number:
				return json.dumps(List)
			else:
				List.append(Title)
				Count+=1
				continue
		if Count>MAX_LOAD:
			Flag_End=1
		else:
			pass
		Page+=1
	return json.dumps(List)
