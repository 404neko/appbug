# -*- coding: UTF-8 -*-

import json
import requests
from _Config import *

def GetMeizu(KeyWord,AppName):
    StoreName=u'魅族商店'
    Key='meizu'
    Url='http://api-app.meizu.com/apps/public/search?&q=%s&os=22'
    Respon=requests.get(Url%(KeyWord)).content
    JSON=json.loads(Respon)
    List=JSON['value']['data']
    Count=0
    for Item in List:
        Count+=1
        if Item['name']==AppName:
            return {'Store':StoreName,'Rank':str(Count),'Key':Key,'KeyWord':KeyWord}
        else:
            continue
    return {'Store':StoreName,'Rank':None,'Key':Key,'KeyWord':KeyWord}

def GetList_Meizu(KeyWord,Number=50):
    Url='http://api-app.meizu.com/apps/public/search?&q=%s&os=22'
    Respon=requests.get(Url%(KeyWord)).content
    JSON=json.loads(Respon)
    List=JSON['value']['data']
    Count=-1
    ReturnList=[]
    while Count<=Number and Count<=len(List):
        Count+=1
        ReturnList.append(List[Count]['name'])
    return ReturnList
