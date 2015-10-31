import time,Queue,threading,AsyncIO

strNow=str(int(time.time()))
AsyncIO.init()

def Refresh():
	global strNow
	strNow=str(int(time.time()))

def PutRaw(Market,Data,KeyWord,Page=1,Time=strNow):
	Refresh()
	SQL='INSERT INTO data.raw(fetchtime,market,data,page,keyword) value("%s","%s","%s","%s","%s")'%(strNow,Market,Data,Page,KeyWord)
	AsyncIO.PutOne_Direct(['Direct',SQL])