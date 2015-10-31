from flask import Flask,session,redirect,url_for,escape,request,render_template,send_from_directory,flash
import os
import hashlib
import MySQLdb
import time
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'A0ZrXUU]LWXX/,98GHJHJ~XHH!jm/jmN*)RT'

Salt_Account_Password='appbug_X/,9'

MySql=MySQLdb.connect('58.96.181.210','root','appbug0','data')

def GetMD5(Data):
	Hash=hashlib.md5()
	Hash.update(Data)
	return Hash.hexdigest()

def Verify(UID,Session):
	Cur=MySql.cursor()
	Cur.execute('SELECT * FROM data.session WHERE session_id="%s" and uid="%s"'%(Session,UID))
	Fin=Cur.fetchall()
	if Fin==():
		return 'NOT_LOGIN',()
	if int(time.time())-Fin[0][4]>int(time.mktime(Fin[0][3].timetuple())):
		Cur.execute('DELETE * FROM data.session WHERE session_id="%s"'%(Session,))
		return 'EXPIRED',Fin[0]
	else:
		return 'SUCCESS',Fin[0]

@app.route('/')
def Index():
	return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path,'static'),'favicon.ico',mimetype='image/vnd.microsoft.icon')

def LoginDashBoard(V_uid,V_session):
	return V_uid+' '+V_session

@app.route('/dashboard')
def DashBoard():
	V_uid=request.cookies.get('uid',False)
	V_session=request.cookies.get('session',False)
	if V_uid and V_session:
		return LoginDashBoard(V_uid,V_session);
	else:
		return Login()

@app.route('/logout')
@app.route('/logoutprocess')
def Logout():
	V_uid=request.cookies.get('uid',False)
	V_session=request.cookies.get('session',False)
	if V_uid and V_session:
		Cur.execute('DELETE * FROM data.session WHERE session_id="%s"'%(Session,))
		response=app.make_response(redirect('/'))
		response.delete_cookie('uid')
		response.delete_cookie('session')
		MySql.commit()
		return response
	else:
		response=app.make_response(redirect('/'))
		return response

@app.route('/reg')
def Reg():
	return render_template('regbox.html')

def osF_RegProcess(Info=None):
	return True

@app.route('/regprocess',methods=['GET', 'POST'])
def RegProcess():
	if request.method=='GET':
		return redirect('/reg')
	else:
		UserName=request.form['username']
		Mail=request.form['mail']
		PassWord=request.form['password']
		agaPassWord=request.form['passwordagain']
		if UserName==None:
			return render_template('regbox.html',Msg='Error: "Username" is empty.',sUserName=UserName,sMail=Mail)
		if PassWord==None:
			return render_template('regbox.html',Msg='Error: "PassWord" is empty.',sUserName=UserName,sMail=Mail)
		if PassWord!=agaPassWord:
			return render_template('regbox.html',Msg='Error: two password are not same.',sUserName=UserName,sMail=Mail)
		if Mail==None:
			return render_template('regbox.html',Msg='Error: "Email" is empty.',sUserName=UserName,sMail=Mail)
		Cur=MySql.cursor()
		Cur.execute("SELECT uid FROM data.account WHERE username='%s' OR email='%s'"%(UserName,Mail))
		Qu=Cur.fetchall()
		print Qu
		if Qu==():
			pass
		else:
			MySql.commit()
			return render_template('regbox.html',Msg='Error: user>%s or mail>%s have exsist.'%(UserName,Mail),sUserName=UserName,sMail=Mail)
		if osF_RegProcess():#INSERT INTO `data`.`account` (`username`) VALUES ('xxx');
			PassWord=GetMD5(PassWord+Salt_Account_Password)
			Cur.execute("INSERT INTO data.account(username,password,email) value('%s','%s','%s')"%(UserName,PassWord,Mail))
			MySql.commit()
			response=app.make_response(redirect('/login'))
			return response
		else:
			psss
		MySql.commit()
		return render_template('regbox.html',Msg='Error: -1',sUserName=UserName,sMail=Mail)

def SetSession(V_uid,request):
	UID=V_uid
	IP=request.remote_addr
	Date=datetime.now()
	w_Time=24*60*60*2
	SideLoad=json.dumps({})
	SessionID=GetMD5(str(UID)+str(IP)+str(Date))
	Cur=MySql.cursor()
	Cur.execute('insert into data.session(session_id,uid,ip,date,w_time,side_load) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(SessionID,UID,IP,Date,w_Time,SideLoad))
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
		Cur.execute('SELECT password,uid FROM account WHERE username="%s"',(UserName,))
		Qu=Cur.fetchall()
		if Qu!=():
			if Qu[0][0]!=PassWord:
				MySql.commit()
				return render_template('loginbox.html',Msg='Error password or username.')
			else:
				V_uid=Qu[0][1]
				T=SetSession(V_uid,request)
				response=app.make_response(redirect('/dashboard'))  
				response.set_cookie('uid',value=str(T[1]))
				response.set_cookie('session',value=str(T[0]))
				MySql.commit()
				return response
		else:
			MySql.commit()
			return render_template('loginbox.html',Msg='User not exsist.')


@app.route('/login')
def Login():
	return render_template('loginbox.html')

app.run(debug=True,host='0.0.0.0')
