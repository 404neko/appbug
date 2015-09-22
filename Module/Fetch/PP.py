# -*- coding: UTF-8 -*-

import json
import requests
from _Config import *

def List(KeyWord,Page):
    #url=http://app.sm.cn/search&str=ua=android&id=12&page=0'&count=30&q='%E7%8C%AB
    return requests.post('http://androidpc.25pp.com/pp_api/sm.php',data={'url':'http://app.sm.cn/search','str':'ua=android&id=12&page='+str(Page)+'&count=30&q='+KeyWord}).content

def NextPage(Credential):
    return int(Credential)+1

def Finder(JObject,AppName):
    List=JObject['items']
    Count=0
    for Item in List:
        Count+=1
        if Item['name']==AppName:
            return [Count,True]
        else:
            continue
    return [Count,False]

def GetPP(KeyWord,AppName):
    StoreName=u'PP 助手'
    Key='pp'
    LoadCount=0
    AppCount=0
    Page=0
    while LoadCount<MAX_LOAD:
        JStr=List(KeyWord,Page)
        JObject=json.loads(JStr)
        if len(JObject['items'])==0:
			break
        Final=Finder(JObject,AppName)
        if Final[1]:
            AppCount+=Final[0]
            return {'Store':StoreName,'Rank':str(AppCount),'Key':Key,'KeyWord':KeyWord}
        else:
            AppCount+=Final[0]
            Page+=1
            LoadCount+=1
    return {'Store':StoreName,'Rank':None,'Key':Key,'KeyWord':KeyWord}

def GetList_PP(KeyWord,Number=50):
    Count=0
    List=[]
    while Count<Number+1:
        JStr=List(KeyWord,Page)
        FullList=json.loads(JStr)['items']
        for Item in FullList:
            List.append(Item['name'])
            Count+=1
            if Count==Number:
                return List
            else:
                continue
    return List