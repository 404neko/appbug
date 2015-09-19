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
        return render_template('index.html')
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
    Results.append( GetWandoujia(KeyWord,AppName) )
    Results.append( GetBaidu(KeyWord,AppName) )
    Results.append( GetXiaomi(KeyWord,AppName) )
    Results.append( GetTencent(KeyWord,AppName) )
    Results.append( Get360(KeyWord,AppName) )
    Results.append( GetAnzhi(KeyWord,AppName) )
    Results.append( GetLenovo(KeyWord,AppName) )
    return Results

#      <p>应用<b>"{{AppName}}"</b>在关键词<b>"{{KeyWords}}"</b>结果的排名情况如下：</p>
#      <div class="hcl-item-box">#
#	  {{Results}}

def sQuery(request):
    KeyWord = request.form.get('word')
    AppName = request.form.get('appname')
    if not KeyWord:
        KeyWord=request.args.get('word')
        AppName=request.args.get('appname')
    if KeyWord:
        KeyWords=KeyWord.replace(u'，',',').split(',')
        Kw4End=copy.deepcopy(KeyWords)
        for i in range(0,len(KeyWords)):
            KeyWords[i]=[KeyWords[i],AppName]
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
        return render_template('srank.html',KeyWords = Kw4End_String,AppName = AppName,Results=html)
    else:
        render_template('srank.html')

def Query(request):
    KeyWord = request.form.get('word')
    AppName = request.form.get('appname')
    if not KeyWord:
        KeyWord=request.args.get('word')
        AppName=request.args.get('appname')
    if KeyWord:
        #+'\n'+GetLenovo(KeyWord,AppName)
        result_rank = []
        '''
        result_rank.append( {'Store':'360','Rank':None,'Key':'360','KeyWord':KeyWord} )
        result_rank.append( {'Store':'3607','Rank':None,'Key':'tencent','KeyWord':KeyWord} )
        result_rank.append( {'Store':u'百度2','Rank':627,'Key':'baidu','KeyWord':KeyWord} )
        result_rank.append( {'Store':'3607','Rank':None,'Key':'360','KeyWord':KeyWord} )
        result_rank.append( {'Store':u'百度1','Rank':627,'Key':'mi','KeyWord':KeyWord} )
        result_rank.append( {'Store':u'百度3','Rank':617,'Key':'baidu','KeyWord':KeyWord} )
        '''
        try:
            result_rank.append( GetWandoujia(KeyWord,AppName) )
            result_rank.append( GetBaidu(KeyWord,AppName) )
            result_rank.append( GetXiaomi(KeyWord,AppName) )
            result_rank.append( GetTencent(KeyWord,AppName) )
            result_rank.append( Get360(KeyWord,AppName) )
            result_rank.append( GetAnzhi(KeyWord,AppName) )
            result_rank.append( GetLenovo(KeyWord,AppName) )
        except:
            pass
        return render_template('rank.html',result_rank = result_rank,KeyWord = KeyWord,AppName = AppName,Get50Host=Get50Host)
    else:
        return render_template('rank.html')

@app.route('/rank/',methods=["POST","GET"])
def Rank():
    KeyWord = request.form.get('word')
    AppName = request.form.get('appname')
    if not KeyWord:
        KeyWord=request.args.get('word')
        AppName=request.args.get('appname')
    if KeyWord:
        if len(KeyWord.replace(u'，',',').split(','))==1:
            return Query(request)
        else:
            return sQuery(request)
    else:
        return render_template('index.html')


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
        return ''
        '''
        FuctionDict={
        'anzhi':GetList_Anzhi(KeyWord),
        'lenovo':GetList_Lenovo(KeyWord),
        '360':GetList_360(KeyWord),
        'mi':GetList_Xiaomi(KeyWord),
        'wandoujia':GetList_Wandoujia(KeyWord),
        'tencent':GetList_Tencent(KeyWord),
        'baidu':GetList_Baidu(KeyWord)
        }
        return FuctionDict[Key]
        '''
    else:
        return ''

if __name__ == '__main__':
    app.run(host='appbug.cn',port=80,threaded=True)
    #app.run(host='127.0.0.1',port=5000,threaded=True,debug=True)
