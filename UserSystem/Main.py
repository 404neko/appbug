from flask import Flask,session,redirect,url_for,escape,request,render_template,send_from_directory
import os
import hashlib
import MySQLdb

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
    if ('uid' in session) and ('session' in session):
        return LoginDashBoard(uid,'session');
    else:
        return Login()

@app.route('/loginprocess',methods=['GET', 'POST'])
def LoginProcess():
    if request.method=='GET':
        return redirect(url_for(Login))
    else:
        UserName=request.form['username']
        PassWord=GetMD5(request.form['password']+Salt_Account_Password)
        Cur=MySql.connection.cursor()
        Cur.execute('''SELECT password FROM account WHERE username=?''',UserName)
        Qu=Cur.fetchall()
        return str(Qu)



@app.route('/login')
def Login():
    return render_template('loginbox.html')

app.run(debug=True)
