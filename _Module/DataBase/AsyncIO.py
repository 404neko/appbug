#-*- coding:utf-8 -*-

import threading
from Queue import Queue
import os
import time
import sys
import MySQLdb

MySql=MySQLdb.connect('localhost','root','appbug0','data')

def Log(String):
	print time.strftime('%I:%M:%S',time.localtime(time.time()))+' - '+String

def DataBaseAction(Data):
	if Data[0]=='Direcrt':
		Cur=MySql.cursor()
	try:
		Cur.execute(Data[1])
		MySql.commit()
		return 0
	except:
		Log('An error occoued when executing sql "'+Data[1]+'".')
		return -1

		

class AsyncIODirect(threading.Thread):
	ToWrite=Queue()

	def __init__(self):
		threading.Thread.__init__(self)
		self.name='AsyncIODirect'

	def run(self):
		while True:
			Data=AsyncIODirect.ToWrite.get()
			DataBaseAction(Data)

def PutOne_Direct(Data):
	AsyncIODirect.ToWrite.put(Data)

def init():
	App=AsyncIODirect()
	App.setDaemon(True)
	App.start()