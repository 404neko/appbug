# -*- coding: UTF-8 -*-

import urllib2, re, time, random
from bs4 import BeautifulSoup
import json
import requests
import sys,os
import gzip
from _Config import *

def GetList_Anzhi(KeyWord,Number=50):
	Url_0='http://m.anzhi.com/search.php?keyword='
	Url_2='&morelist='
	Page=0
	Flag_End=0
	Magnification=1
	Count=1
	List=[]
	while Flag_End==0:
		Url=Url_0+KeyWord+Url_2+str(Page)
		Result=requests.get(Url,headers=Headers).content
		BeautifulSoup_items=BeautifulSoup(Result).findAll('li')[5:]
		if len(BeautifulSoup_items)==0:
			Flag_End=1
			continue
		else:
			pass
		for Item in BeautifulSoup_items:
			Title=Item.find('h4').text
			if Count>=Number:#if Title==unicode(AppName,'UTF-8'):
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

def GetAnzhi(KeyWord,AppName):
	#
	Key='anzhi'
	StoreName=u'安智市场'
	Url_0='http://m.anzhi.com/search.php?keyword='
	Url_2='&morelist='
	Page=0
	Flag_End=0
	Magnification=1
	Count=1
	while Flag_End==0:
		Url=Url_0+KeyWord+Url_2+str(Page)
		Result=requests.get(Url,headers=Headers).content
		BeautifulSoup_items=BeautifulSoup(Result).findAll('li')[5:]
		if len(BeautifulSoup_items)==0:
			Flag_End=1
			continue
		else:
			pass
		for Item in BeautifulSoup_items:
			Title=Item.find('h4').text
			if Title==AppName:#if Title==unicode(AppName,'UTF-8'):
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
