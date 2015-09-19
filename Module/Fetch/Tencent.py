# -*- coding: UTF-8 -*-

import urllib2, re, time, random
from bs4 import BeautifulSoup
import json
import requests
import sys,os
import gzip
from _Config import *

def GetTencent(KeyWord,AppName):
	def NameUtil():
		pass
	StoreName=u'应用宝'
	Key='tencent'
	Url_0='http://android.myapp.com/myapp/searchAjax.htm?kw='
	Url_2='&pns='
	Url_4='&sid='
	Url_Sid=''
	Url_pns=''
	Page=0
	Flag_End=0
	Magnification=1
	Count=1
	while Flag_End==0:
	#if True:
		Url=Url_0+KeyWord+Url_2+Url_pns+Url_4+str(Url_Sid)
		Result=requests.get(Url,headers=Headers).content
		Result=json.loads(Result)
		Json_items=Result['obj']['appDetails']
		Url_Sid=Result['obj']['searchId']
		Url_pns=Result['obj']['pageNumberStack']
		if len(Json_items)==0:
			Flag_End=1
			continue
		else:
			pass
		for Item in Json_items:
			Title=Item['appName']
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

def GetList_Tencent(KeyWord,Number=50):
	def NameUtil():
		pass
	Url_0='http://android.myapp.com/myapp/searchAjax.htm?kw='
	Url_2='&pns='
	Url_4='&sid='
	Url_Sid=''
	Url_pns=''
	Page=0
	Flag_End=0
	Magnification=1
	Count=1
	List=[]
	while Flag_End==0:
	#if True:
		Url=Url_0+KeyWord+Url_2+Url_pns+Url_4+str(Url_Sid)
		Result=requests.get(Url,headers=Headers).content
		Result=json.loads(Result)
		Json_items=Result['obj']['appDetails']
		Url_Sid=Result['obj']['searchId']
		Url_pns=Result['obj']['pageNumberStack']
		if len(Json_items)==0:
			Flag_End=1
			continue
		else:
			pass
		for Item in Json_items:
			Title=Item['appName']
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
