from flask import Flask,session,redirect,url_for,escape,request,render_template,send_from_directory
import os
import hashlib
import MySQLdb
import time
import json

app = Flask(__name__)
app.secret_key = 'A0ZrXUU]LWXX/,98GHJHJ~XHH!jm/jmN*)RT'

Salt_Account_Password='appbug_X/,9'

MySql=MySQLdb.connect('localhost','root','appbug0','data')

def GetMD5(Data):
	Hash=hashlib.md5()
	Hash.update(Data)
	return Hash.hexdigest()

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path,'static'),'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/dashboard')
def DashBoard():
	V_uid=request.cookies.get('uid',False)
	V_session=request.cookies.get('session',False)
	if V_uid and V_session:
		return LoginDashBoard(V_uid,V_session);
	else:
		return Login()

def SetSession(V_uid,request):
	UID=V_uid
	IP=request.remote_addr
	Date=int(time.time())
	w_Time=24*60*60*2
	SideLoad=json.dumps({})
	SessionID=GetMD5(str(UID)+str(IP)+str(Date))
	Cur=MySql.cursor()

	Cur.execute('insert into session(session_id,uid,ip,date,w_time,side_load) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(SessionID,UID,IP,Date,w_Time,SideLoad))
	MySql.commit()
	return SessionID,UID,IP,Date,w_Time,SideLoad

@app.route('/loginprocess',methods=['GET', 'POST'])
def LoginProcess():
	if request.method=='GET':
		return redirect(url_for(Login))
	else:
		UserName=request.form['username']
		PassWord=GetMD5(request.form['password']+Salt_Account_Password)
		Cur=MySql.cursor()
		Cur.execute('SELECT password,uid FROM account WHERE username=%s',(UserName,))
		Qu=Cur.fetchall()
		if Qu!=():
			if Qu[0][0]!=PassWord:
				return render_template('loginbox.html',Msg='Error password or username.')
			else:
				V_uid=Qu[0][1]
				T=SetSession(V_uid,request)
				S=''
				for i in T:
					S+=str(i)
				return S


@app.route('/login')
def Login():
	return render_template('loginbox.html')

app.run(debug=True,host='0.0.0.0')
