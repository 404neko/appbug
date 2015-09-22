# -*- coding: UTF-8 -*-

#>all the imports
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
import urllib2, re, time, random
from bs4 import BeautifulSoup
import json
import requests
import sqlite3
import sys,os
from Module.Fetch import *
import copy

#deal with coding
#reload(sys)
#sys.setdefaultencoding('utf8')

#>database init(sqlite)
DATABASE = 'pl.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
Get50Host='http://127.0.0.1:5000/'

#>init flask
app = Flask(__name__)
app.config.from_object(__name__)

#>deal with db connect
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
#def init_db():
#    with closing(connect_db()) as db:
#        with app.open_resource('schema.sql') as f:
#            db.cursor().executescript(f.read())
#        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()





#>index
@app.route('/',methods=["POST","GET"])
def show_index():
    keyword = request.form.get('title')
    if keyword:
        return redirect('/'+keyword)
    else :
        return render_template('index.html',Raw_Checkbox=Raw_Checkbox)
#q
"""
@app.route('/<keyword>',methods=["POST","GET"])
def show_search(keyword):
    keyword = '%' + keyword + '%'
    cur = g.db.execute('''select app_name from app_id where app_name like '%s' order by app_name''' % keyword)
    search_list = [dict(app_name=row[0]) for row in cur.fetchall()]
    return render_template('search_list.html', search_list = search_list)
"""
#q and db
#@app.route('/s/<keyword>')
#def show_search(keyword):
#    keyword = '%' + keyword + '%'
#    cur = g.db.execute('''select APP_NAME from qg where app_name like '%s' ''' % keyword)
#    search_list = [dict(APP_NAME=row[0]) for row in cur.fetchall()]
#    return render_template('search_list.html', search_list = search_list)


@app.route('/app/<appname>')
def show_dx(appname):
    cur = g.db.execute("select COMMENTS, NUM from dx WHERE APP_NAME = '%s'  order by date desc limit 10" % appname)
    entries = [dict(COMMENTS=row[0], NUM=row[1]) for row in cur.fetchall()]
    #return render_template('layout.html', entries=entries)
    cur = g.db.execute("select VERSION, COMMENT,DATE from qg WHERE APP_NAME = '%s' order by DATE desc " % appname)
    qgs = [dict(VERSION=row[0], COMMENT=row[1], DATE=row[2]) for row in cur.fetchall()]
    return render_template('layout.html', entries=entries, qgs=qgs)

def QueryTask(Val):
    Results=[]
    KeyWord=Val[0]
    AppName=Val[1]
    EnabledKey=Val[2]
    result_rank = []
    for aKey in EnabledKey:
        result_rank.append( KeyList[aKey]['Fuction'](KeyWord,AppName) )
    '''
    Results.append( GetWandoujia(KeyWord,AppName) )
    Results.append( GetBaidu(KeyWord,AppName) )
    Results.append( GetXiaomi(KeyWord,AppName) )
    Results.append( GetTencent(KeyWord,AppName) )
    Results.append( Get360(KeyWord,AppName) )
    Results.append( GetAnzhi(KeyWord,AppName) )
    Results.append( GetLenovo(KeyWord,AppName) )
    '''
    return result_rank

#      <p>应用<b>"{{AppName}}"</b>在关键词<b>"{{KeyWords}}"</b>结果的排名情况如下：</p>
#      <div class="hcl-item-box">#
#	  {{Results}}

def sQuery(request,EnabledKey):
    KeyWord = request.form.get('word')
    AppName = request.form.get('appname')
    #if not KeyWord:
#        KeyWord=request.args.get('word')
#        AppName=request.args.get('appname')
    if KeyWord:
        KeyWords=KeyWord.replace(u'，',',').split(',')
        Kw4End=copy.deepcopy(KeyWords)
        for i in range(0,len(KeyWords)):
            KeyWords[i]=[KeyWords[i],AppName,EnabledKey]
        Results=map(QueryTask,KeyWords)
        midRes={}
        for ResultItem in Results:
            for aResult in ResultItem:
                if midRes.get(aResult['Store'],-1)==-1:
                    midRes[aResult['Store']]={}
                    midRes[aResult['Store']][aResult['KeyWord']]=aResult['Rank']
                else:
                    midRes[aResult['Store']][aResult['KeyWord']]=aResult['Rank']
        html=u'<span>关键词</span>\n'
        KwDict={}
        for ShopName in midRes:
            for Kws in midRes[ShopName]:
                KwDict[Kws]=''
            toAdd='<span>'+ShopName+'</span>\n'
            html+=toAdd
        html+='<br>'
        for aKw in KwDict:
            toAdd='<span>'+aKw+'</span>\n'
            html+=toAdd
            for ShopName in midRes:
                Rank=midRes[ShopName].get(aKw,' ')
                toAdd='<span>'+str(Rank)+'</span>\n'
                html+=toAdd
            html+='<br>'
        html=html[:-4]
        Kw4End_String=','.join(Kw4End)
        return render_template('srank.html',KeyWords = Kw4End_String,AppName = AppName,Results=html,Raw_Checkbox=Raw_Checkbox)
    else:
        render_template('srank.html')

def Query(request,EnabledKey):
    KeyWord = request.form.get('word')
    AppName = request.form.get('appname')
    #if not KeyWord:
#        KeyWord=request.args.get('word')
#        AppName=request.args.get('appname')
    if KeyWord:
        #+'\n'+GetLenovo(KeyWord,AppName)
        result_rank = []
        if 1:#try:
            for aKey in EnabledKey:
                result_rank.append( KeyList[aKey]['Fuction'](KeyWord,AppName) )
        else:#except:
            pass
        return render_template('rank.html',result_rank = result_rank,KeyWord = KeyWord,AppName = AppName,Get50Host=Get50Host,Raw_Checkbox=Raw_Checkbox)
    else:
        return render_template('rank.html')

@app.route('/rank/',methods=["POST"])
def Rank():
    KeyWord = request.form.get('word')
    AppName = request.form.get('appname')
    #if not KeyWord:
    #    print '================================='
    #    KeyWord=request.args.get('word')
    #    AppName=request.args.get('appname')
    EnabledKey=[]
    for aKey in KeyList:
        if request.form.get(aKey)!=None:
            EnabledKey.append(aKey)
    if KeyWord:
        if len(KeyWord.replace(u'，',',').split(','))==1:
            return Query(request,EnabledKey)
        else:
            return sQuery(request,EnabledKey)
    else:
        return render_template('index.html',Raw_Checkbox=Raw_Checkbox)


@app.route('/api/get50',methods=["POST","GET"])
def Get50():
    Key=request.form.get('Key')
    KeyWord=request.form.get('KeyWord')
    if not Key:
        Key=request.args.get('Key')
        KeyWord=request.args.get('KeyWord')
    if Key and KeyWord:#+'\n'+GetLenovo(KeyWord,AppName)
        if Key=='anzhi':
            return GetList_Anzhi(KeyWord)
        if Key=='lenovo':
            return GetList_Lenovo(KeyWord)
        if Key=='360':
            return GetList_360(KeyWord)
        if Key=='mi':
            print KeyWord
            return GetList_Xiaomi(KeyWord)
        if Key=='wandoujia':
            return GetList_Wandoujia(KeyWord)
        if Key=='tencent':
            return GetList_Tencent(KeyWord)
        if Key=='baidu':
            return GetList_Baidu(KeyWord)
        if Key=='pp':
            return GetList_PP(KeyWord)
        if Key=='hiapk':
            return GetList_Hiapk(KeyWord)
        if Key=='meizu':
            return GetList_Meizu(KeyWord)
        return ''
    else:
        return ''

if __name__ == '__main__':
    PluginInfo=[
                {'StoreName':u'百度手机助手','Key':'baidu','Fuction':GetBaidu},
                {'StoreName':u'乐商店','Key':'lenovo','Fuction':GetLenovo},
                {'StoreName':u'安智市场','Key':'anzhi','Fuction':GetAnzhi},
                {'StoreName':u'小米应用商店','Key':'mi','Fuction':GetXiaomi},
                {'StoreName':u'360 手机助手','Key':'360','Fuction':Get360},
                {'StoreName':u'豌豆荚','Key':'wandoujia','Fuction':GetWandoujia},
                {'StoreName':u'应用宝','Key':'tencent','Fuction':GetTencent},
                {'StoreName':u'PP 助手','Key':'pp','Fuction':GetPP},
                {'StoreName':u'安卓市场','Key':'hiapk','Fuction':GetHiapk},
                {'StoreName':u'魅族商店','Key':'meizu','Fuction':GetMeizu}
                ]
    Raw_Checkbox=''
    KeyList={}
    CheckBox='<label><input type="checkbox" checked="%s" value="1" class="form-checkbox" name="%s"><span>%s</span></label>'
    for aPlugin in PluginInfo:
        Raw_Checkbox+=CheckBox%('checked',aPlugin['Key'],aPlugin['StoreName'])
        Raw_Checkbox+='\n'
        KeyList[aPlugin['Key']]={'StoreName':aPlugin['StoreName'],'Fuction':aPlugin['Fuction']}
    app.run(host='127.0.0.1',port=5000,threaded=True,debug=True)
    #app.run(host='appbug.cn',port=80,threaded=True)
