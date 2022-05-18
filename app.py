from flask import Flask,render_template,request,redirect,url_for,session
from flask_pymongo import pymongo
from flask_pymongo import PyMongo
#from cryptography.fernet import Fernet
import os
from decouple import config
#key=Fernet.generate_key()
#salt=key.decode('utf8')

#try:
  #app=Flask(__name__)
  #CONNECTION_STRING = "mongodb+srv://birla:birlahostel@mithostel.ss3nh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
  #client = pymongo.MongoClient(CONNECTION_STRING)
  #db = client.get_database('mithostel')
  #records=db.user
  ##app.config['MONGO_URI']="mongodb://localhost:27017/manager"
  ##mongo=PyMongo(app)
#
#
  #@app.route("/",methods=["POST","GET"])
  #def log():
    #return render_template("electricity_form.html")
  #@app.route("/signup",methods=["POST","GET"])
  #def signup():
    #return render_template("register.html")
#
  #@app.route("/register",methods=["POST","GET"])
  #def reg():
    #message=''
    #if request.method =='POST':
      #u=request.form['id']
      #e=request.form['mail']
      #pw=request.form['pwd']
      #rpw=request.form['repwd']
      #em=str(e).lower()
      #ur=str(u).lower()
      #obj=pw.encode()
      #instance=salt.encode()
      #crypter=Fernet(instance)
      #bush=crypter.encrypt(obj)
      #k=str(bush,'utf8')
#
      #users=records.find({})
#      
      #for x in users:
        #usr=x['username']
        #if usr == ur:
          #message="Username already exists"
          #return render_template("register.html",msg=message)
      #if pw != rpw:
        #message="Password doesn't match"
        #return render_template("register.html",msg=message)
      #else:
        #users=records.insert_one({"username":ur,"email":em,"password":k,"salt":salt})
        #return render_template("login.html") 
#  
  #@app.route("/allow",methods=["POST","GET"])
  #def allow():
    #message=''
    #flag=0
    #if request.method == "POST":
      #u=request.form["id"]
      #pas=request.form["key"]
      #name=str(u).lower()
      #users=records.find({})
      #for x in users:
        #n=x['username']
        #if n == name:
          #flag=1
      #if(flag==0):
        #message="Invalid Username"  
        #return render_template("login.html",msg=message) 
      #user=records.find({"username":name})
      #for x in user:
        #pwd=x['password']
        #sss=x['salt']
        #s=pwd.encode()
        #instance=sss.encode()
        #crypter=Fernet(instance)
        #decryptpw=crypter.decrypt(s)
        #returned=decryptpw.decode('utf8')
        #if returned == pas:
          #return render_template("success.html")
        #else:
          #message="Invalid Password"  
          #return render_template("login.html",msg=message) 
#
#except Exception as e:
  #print(e)



app = Flask(__name__)

# app configs
app.config['MONGO_URI'] = "mongodb+srv://birla:birlahostel@mithostel.ss3nh.mongodb.net/mithostel?retryWrites=true&w=majority"

mongo = PyMongo(app)
book  = mongo.db['user'] 

@app.route("/",methods=["POST","GET"])
def log():
  return render_template("electricity_form.html")

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
    print("h2")
    contact_obj = {
        "registerno"      : registerno,
        "studentname"     : studentname,
        "pnumber"     : pnumber,
        "hblock"     : hblock,
        "rnumber"     : rnumber,
        "issuedetail"     : issuedetail,
        "issuefaced" : issuefaced,
        "atime"     : atime
    }
       
    book.insert_one(contact_obj)

    #  mongo.db['telephone-registry'].insert_one({"name":"Naveen","place":"Chennai"})

    result_dict = {
        "Status" : "Contact Inserted Successfully"
    }

    return result_dict

if __name__ == "main":
  app.run(debug=True)