# -*- coding: UTF-8 -*-

import urllib2, re, time, random
from bs4 import BeautifulSoup
import json
import requests
import sys,os
import gzip
from _Config import *

def GetList_Xiaomi(KeyWord,Number=50):
	def NameUtil():
		pass
	Url_0='http://app.market.xiaomi.com/apm/search?&clientId=23e4975185081fb8ddb6b24fd4745395&co=CN&keyword='
	Url_2='&la=zh&os=C92B186&page='
	Url_4='&ref=input&resolution=540*960&sdk=18'
	Page=0
	Flag_End=0
	Magnification=1
	Count=1
	List=[]
	while Flag_End==0:
	#if True:
		Url=Url_0+KeyWord+Url_2+str(Page)+Url_4
		Result=requests.get(Url,headers=Headers).content
		Result=json.loads(Result)
		Json_items=Result['listApp']
		if len(Json_items)==0:
			Flag_End=1
			continue
		else:
			pass
		for Item in Json_items:
			Title=Item['displayName']
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

def GetXiaomi(KeyWord,AppName):
	def NameUtil():
		pass
	StoreName=u'小米应用商店'
	Key='mi'
	Url_0='http://app.market.xiaomi.com/apm/search?&clientId=23e4975185081fb8ddb6b24fd4745395&co=CN&keyword='
	Url_2='&la=zh&os=C92B186&page='
	Url_4='&ref=input&resolution=540*960&sdk=18'
	Page=0
	Flag_End=0
	Magnification=1
	Count=1
	while Flag_End==0:
	#if True:
		Url=Url_0+KeyWord+Url_2+str(Page)+Url_4
		Result=requests.get(Url,headers=Headers).content
		Result=json.loads(Result)
		Json_items=Result['listApp']
		if len(Json_items)==0:
			Flag_End=1
			continue
		else:
			pass
		for Item in Json_items:
			Title=Item['displayName']
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
