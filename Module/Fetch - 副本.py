# -*- coding: UTF-8 -*-

from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash
import urllib2, re, time, random
from bs4 import BeautifulSoup
import json
import requests
import sqlite3
import sys,os

MAX_LOAD=20
Headers={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
	}

SendMesg='{"lang":"zh-CN","channel":"12346","cta":"false","deviceIdType":"imei","deviceId":"802A8904","deviceBrand":"Huawei","deviceManufacturer":"HUAWEI","deviceModel":"HUAWEI+C8816","density":"1.5","dpi":"240","horizontalResolution":"540","verticalResolution":"960","os":"android","osVersion":"4.3","sdkVersion":"18","clientVersion":"7.1.30.88","clientVersionCode":70130,"packageName":"android%3Acom.lenovo.leos.appstore-7.1.30.88","cpu":"armeabi-v7a","od":"18","phoneNumber1":"","phoneNumber2":"","simoperator1":"46003","simoperator2":"","iccid":"89860314704290341196","imsi":"460030986722367","fsp":"1","clientid":"","st":"","latitude":"","longitude":"","nettype":"WIFI"}'

global Cookie_Lenovo
Cookie_Lenovo={
'clientid':'58168-2-2-18-1-3-1_240_i802A8904t19700211111518174_c19251d1p1'
}

import gzip
def GZString(String):
	File=gzip.open('File.gz','wb')
	File.write(String)
	File.close()
	File=open('File.gz','rb')
	Raw=File.read()
	File.close()
	return Raw

def GetClientID(SendMesg=SendMesg):
	ToPost=GZString(SendMesg)
	Cookie={'pn':'com.lenovo.leos.appstore','vn':'7.1.30.88','vc':'70130','channelid':'12346','virtualDeviceId':'','lpsust':'null','clientid':'null','seqno':'203386'}
	Url='http://223.202.25.30/ams/api/register?l=zh-CN&v=2'
	Result=requests.post(Url,cookies=Cookie,data=ToPost)
	Json=json.loads(Result.content)
	Aim=Json['clientid']
	return Aim

def GetLenovo(KeyWord,AppName):
	def NameUtil():
		pass
	global Cookie_Lenovo
	StoreName=u'乐商店'
	Key='lenovo'
	Url_0='http://223.202.25.30/ams/3.0/appsearchdata.do?l=zh-CN&k='
	Url_2='&si='
	Page=1
	Flag_End=0
	Magnification=1
	Count=1
	while Flag_End==0:
		Url=Url_0+KeyWord+Url_2+str(Page)
		Result=requests.get(Url,headers=Headers,cookies=Cookie_Lenovo).content
		try:
			Result=json.loads(Result)
			Json_items=Result['datalist']
		except:
			Cookie_Lenovo['clientid']=GetClientID()
			Result=requests.get(Url,headers=Headers,cookies=Cookie_Lenovo).content
			Result=json.loads(Result)
			Json_items=Result['datalist']
		if len(Json_items)==0:
			Flag_End=1
			continue
		else:
			pass
		for Item in Json_items:
			Title=Item['appname']
			if Title==AppName:#render_template('rank.html',result_rank = result_rank,KeyWord = KeyWord,AppName = AppName)
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

def GetList_Lenovo(KeyWord,Number=50):
	def NameUtil():
		pass
	global Cookie_Lenovo
	Url_0='http://223.202.25.30/ams/3.0/appsearchdata.do?l=zh-CN&k='
	Url_2='&si='
	Page=0
	Flag_End=0
	Magnification=1
	Count=1
	List=[]
	while Flag_End==0:
		Url=Url_0+KeyWord+Url_2+str(Page)
		Result=requests.get(Url,headers=Headers,cookies=Cookie_Lenovo).content
		try:
			Result=json.loads(Result)
			Json_items=Result['datalist']
		except:
			Cookie_Lenovo['clientid']=GetClientID()
			Result=requests.get(Url,headers=Headers,cookies=Cookie_Lenovo).content
			Result=json.loads(Result)
			Json_items=Result['datalist']
		if len(Json_items)==0:
			print len(Json_items)
			Flag_End=1
			continue
		else:
			pass
		for Item in Json_items:
			Title=Item['appname']
			if Count>=Number:
				return json.dumps(List)

			else:
				Count+=1
				List.append(Title)
				continue
		Page+=1
	return json.dumps(List)

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
				return render_template('rank_Item.html',Store=StoreName,Rank=str(Count),KeyWord=KeyWord,Key=Key)
			else:
				Count+=1
				continue
		if Count>MAX_LOAD:
			Flag_End=1
		else:
			pass
		Page+=1
	return {'Store':StoreName,'Rank':None,'Key':Key,'KeyWord':KeyWord}

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

def GetBaidu(KeyWord,AppName):
	Url_0='http://m.baidu.com/s?&tn=native&ver=16785292&platform_version_id=18&st=10a0011&word='
	Url_2='&pn='
	StoreName=u'百度手机助手'
	Page=0
	Key='baidu'
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

def GetList_Baidu(KeyWord,Number=50):
	Url_0='http://m.baidu.com/s?&tn=native&ver=16785292&platform_version_id=18&st=10a0011&word='
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