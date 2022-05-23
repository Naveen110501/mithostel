from flask import Flask,render_template,request,redirect,url_for,session

from flask_pymongo import PyMongo
from cryptography.fernet import Fernet
import os
from decouple import config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import pytz

block_one="one"
login_id=""
IST = pytz.timezone('Asia/Kolkata')

key=Fernet.generate_key()
salt=key.decode('utf8')


app = Flask(__name__)


app.config['MONGO_URI'] = "mongodb+srv://birla:birlahostel@mithostel.ss3nh.mongodb.net/mithostel?retryWrites=true&w=majority"

mongo = PyMongo(app)
complain  = mongo.db['user'] 
records=mongo.db['login'] 

@app.route("/",methods=["POST","GET"])
def log():
  return render_template("login.html")

    
@app.route("/signup", methods = ["POST", "GET"])
def signup():
  return render_template("register.html")

@app.route("/login", methods = ["POST", "GET"])
def login():
  return render_template("login.html")

@app.route("/reset", methods = ["POST", "GET"])
def reset():
  return render_template("reset.html")

@app.route("/electricity", methods = ["POST", "GET"])
def electricity():
  return render_template("electricity_form.html")

@app.route("/register", methods = ["POST","GET"])
def reg():

  message = ''
  usr=''

  if request.method == 'POST':


    userid = request.form['emailname']
    studentname = request.form['sname']
    emailid = request.form['ename']
    hostelblock = request.form['hostelblock']
    password = request.form['password']
    r_password = request.form['cpassword']

    
    obj = password.encode()

    instance = salt.encode()
    crypter = Fernet(instance)
    bush = crypter.encrypt(obj)
    k = str(bush, 'utf8')

    users = records.find({})
      
    for x in users:
      usr = x['Register Number']

    if usr == userid:
      message = "Register Number already exists"
      return render_template("login.html", msg = message)

    if password != r_password:
      message = "Password doesn't match"
      return render_template("login.html", msg = message)
    
    else:
      users = records.insert_one({"Register Number" : userid, "Student Name" : studentname,"Email Id":emailid,"hostelblock":hostelblock, "password" : k, "salt" : salt})
      message="Account Created Successfully"  
      return render_template("login.html",msg=message) 
  
@app.route("/allow", methods = ["POST", "GET"])
def allow():
  message=''
  flag=0
  global login_id
  if request.method == "POST":
    u=request.form["id"]
    pas=request.form["key"]
    users=records.find({})
    for x in users:
      n=x['Register Number']
      if n == u:
        flag=1
    if(flag==0):
      message="Invalid Register Number"  
      return render_template("login.html",msg=message) 
      
    user=records.find({"Register Number":u})
    for x in user:
      pwd=x['password']
      sss=x['salt']
      s=pwd.encode()
      instance=sss.encode()
      crypter=Fernet(instance)
      decryptpw=crypter.decrypt(s)
      returned=decryptpw.decode('utf8')
      if returned == pas:
        login_id=u
        return redirect(url_for("get_complain_history"))
      else:
        message="Invalid Password"  
        return render_template("login.html",msg=message) 


@app.route("/reset-password", methods = ["POST", "GET"])
def reset_password():
  message=''
  flag=0
  em=0
  global login_id
  if request.method == "POST":
    u=request.form["id"]
    pas=request.form["key"]
    users=records.find({})
    for x in users:
      n=x['Register Number']
      email_id=x['Email Id']
      pwd=x['password']
      sss=x['salt']
      s=pwd.encode()
      instance=sss.encode()
      crypter=Fernet(instance)
      decryptpw=crypter.decrypt(s)
      returned=decryptpw.decode('utf8')
      if n == u:
        flag=1
      if email_id == pas:
        em=1
    
    if(flag==0):
      message="Invalid Register Number"  
      return render_template("login.html",msg=message) 

    if(em==0):
      message="Invalid Email Id"  
      return render_template("login.html",msg=message) 

    else:
      fromaddr = "birla.mit.h@gmail.com"
      toaddr = "naveenvellaiyappan02@gmail.com"
      body_msg=returned
      msg = MIMEMultipart()
      msg['From'] = fromaddr
      msg['To'] = toaddr
      msg['Subject'] = "Forget Password"
      body = body_msg
      msg.attach(MIMEText(body, 'plain'))
      s = smtplib.SMTP('smtp.gmail.com', 587)
      s.starttls()
      s.login(fromaddr, "mithostelbirla")
      text = msg.as_string()
      s.sendmail(fromaddr, toaddr, text)
      s.quit()

      message="Password Sent to Registered Email Id Successfully"  
      return render_template("login.html",msg=message) 
      


@app.route("/add_new_complain",methods = ["POST","GET"])
def add_new_complain():
    
  if request.method =='POST':
    registerno  = request.form['registerno']
    studentname = request.form['studentname']
    pnumber = request.form['pnumber']
    hblock = request.form['hblock']
    rnumber = request.form['rnumber']
    issuedetail = request.form['issuedetail']
    issuefaced = request.form['issuefaced']
    atime = request.form['atime']

   
    if login_id != registerno:
      message="Invalid Register Number"  
      return render_template("login.html",msg=message) 
      
    complains = complain.find()

    for x in complains:
      n=x['Register Number']
      hblock_id=x['Hostel Block']
      r_number=x['Room Number']
      issue_faced=x['Issue Faced']
      status=x['Status']
      if registerno==n and hblock==hblock_id and rnumber==r_number and issuefaced==issue_faced and status=="Pending":
        message="Complain Already Registered"
        return render_template("electricity_form.html",msg=message) 

      
    complain_obj = {
        "Register Number"      : registerno,
        "Student Name"     : studentname,
        "Phone Number"     : pnumber,
        "Hostel Block"     : hblock,
        "Room Number"     : rnumber,
        "Issue Detail"     : issuedetail,
        "Issue Faced" : issuefaced,
        "Avalability Time"     : atime,
        "Status":"Pending",
        "Time":datetime.now(IST)
    }
      
    complain.insert_one(complain_obj)

    message="Complain Registered Successfully"
    return render_template("electricity_form.html",msg=message) 
    


@app.route("/get-all-complain",methods = ['GET','POST'])
def get_all_complain():

  global block_one
  complains=""
  complain_year = complain.distinct('Hostel Block')

  hblock_list = []
  hblock_obj = {}
  
  for item in complain_year :
      hblock_obj = {
      'hblock' : item 
      }
      hblock_list.append(hblock_obj)


  room_year = complain.distinct('Room Number')
  issue_year = complain.distinct('Issue Faced')

  contact_list = []
  year_list = []
  contact_obj = {}
  year_obj = {}

  for item in issue_year :
    contact_obj = {
      'month' : item 
    }
    contact_list.append(contact_obj)

  for item in room_year :
    year_obj = {
      'year' : item 
    }
    year_list.append(year_obj)


  contacts_month = complain.distinct('Status')

  status_list = []
  contact_obj = {}


  for item in contacts_month :
    contact_obj = {
      'month' : item 
    }
    status_list.append(contact_obj)

  f_hblock=block_one

  if request.method =='POST':
    hblock  = request.form['hblock']
    room = request.form['room']
    issue = request.form['issue']
    status = request.form['status']
    if hblock!=" " and hblock!="Hostel Block":
      complains = complain.find({ 'Hostel Block' : hblock })
    elif room!=" " and room!="Room Number":
      complains = complain.find({ 'Room Number' : room })
    elif issue!=" " and issue!="Issue":
      complains = complain.find({ 'Issue Faced' : issue })
    elif status!=" " and status!="Status":
      complains = complain.find({ 'Status' : status })


    else:
      complains = complain.find()

  complain_list = []
  for item in complains:
      complain_obj = {
          "registerno"      : item['Register Number'],
          "studentname"     : item['Student Name'],
          "pnumber"     : item['Phone Number'],
          "hblock"     : item['Hostel Block'],
          "rnumber"     : item['Room Number'],
          "issuedetail"     : item['Issue Detail'],
          "issuefaced" : item['Issue Faced'],
          "atime"     : item['Avalability Time'],
          "status"     : item['Status']
      }
      complain_list.append(complain_obj)


  return render_template('ntable.html', rows_data = complain_list, block_data = hblock_list ,status_data=status_list,contact_data=contact_list,year_data=year_list)


@app.route("/get-complain-history",methods = ['GET'])
def get_complain_history():
  global login_id
  print(login_id)
  complains = complain.find({ 'Register Number' : login_id })

  complain_list = []

  for item in complains:
      complain_obj = {
          "registerno"      : item['Register Number'],
          "studentname"     : item['Student Name'],
          "pnumber"     : item['Phone Number'],
          "hblock"     : item['Hostel Block'],
          "rnumber"     : item['Room Number'],
          "issuedetail"     : item['Issue Detail'],
          "issuefaced" : item['Issue Faced'],
          "atime"     : item['Avalability Time'],
          "status"     : item['Status']
      }
      complain_list.append(complain_obj)


  return render_template('stable.html', rows_data = complain_list )


@app.route("/vary-block/<v>",methods=["POST","GET"])
def vary_block(v):

    check=v.split(',')
    complain.update_one({"Register Number":check[2],"Room Number":check[0],"Issue Faced":check[1]},{"$set":{"Status":"Solved"}})
    message="Status Updated Successfully"
    return redirect(url_for("get_all_complain")) 

if __name__ == "main":
  
  print("hi")
  app.run(debug=True)