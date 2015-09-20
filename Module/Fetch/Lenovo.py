# -*- coding: UTF-8 -*-

import urllib2, re, time, random
from bs4 import BeautifulSoup
import json
import requests
import sys,os
import gzip
from _Config import *

global Cookie_Lenovo
Cookie_Lenovo={
                'clientid':'58168-2-2-18-1-3-1_240_i802A8904t19700211111518174_c19251d1p1'
                }

SendMesg='{"lang":"zh-CN","channel":"12346","cta":"false","deviceIdType":"imei","deviceId":"802A8904","deviceBrand":"Huawei","deviceManufacturer":"HUAWEI","deviceModel":"HUAWEI+C8816","density":"1.5","dpi":"240","horizontalResolution":"540","verticalResolution":"960","os":"android","osVersion":"4.3","sdkVersion":"18","clientVersion":"7.1.30.88","clientVersionCode":70130,"packageName":"android%3Acom.lenovo.leos.appstore-7.1.30.88","cpu":"armeabi-v7a","od":"18","phoneNumber1":"","phoneNumber2":"","simoperator1":"46003","simoperator2":"","iccid":"89860314704290341196","imsi":"460030986722367","fsp":"1","clientid":"","st":"","latitude":"","longitude":"","nettype":"WIFI"}'

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
{'StoreName':u'百度手机助手','Key':'baidu'},{'StoreName':u'乐商店','Key':'lenovo'},{'StoreName':u'百度手机助手','Key':'baidu'}
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
