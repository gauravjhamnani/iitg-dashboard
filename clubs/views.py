# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.


import pyrebase
#from pyrebase_settings import db,auth
config = {
  # "apiKey": "apiKey",
  # "authDomain": "projectId.firebaseapp.com",
  # "databaseURL": "https://databaseName.firebaseio.com",
  # "storageBucket": "projectId.appspot.com",
  # "serviceAccount": "path/to/serviceAccountCredentials.json"
    "apiKey": "AIzaSyBKpkIggXwQujW_9M7v01tVH-UyWN9CbcA",
    "authDomain": "hackriti-110f1.firebaseapp.com",
    "databaseURL": "https://hackriti-110f1.firebaseio.com",
    "projectId": "hackriti-110f1",
    "storageBucket": "hackriti-110f1.appspot.com",
    "messagingSenderId": "449573222649"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()
def index(request):
	return render(request,'clubs/index.html')

def signin(request):
	return render(request,'clubs/signin.html')

def postsign(request):
	email=request.POST.get('email')
	passw = request.POST.get("pass")
	try:
		user = auth.sign_in_with_email_and_password(email,passw)
	except:
		message = "invalid cerediantials"
		return render(request,"clubs/signin.html",{"msg":message})
	return render(request, "clubs/index.html",{"e":email})

def addclub(request):
	if request.method == "POST":
		clubname = request.POST('clubname')
		email = request.POST('email')
		password = request.POST('password')
		auth.create_user_with_email_and_password(email, password)
		dic={
			"email" : email,
			"Photo": None,
			"Desc" : None,
			"Res" : None,
			"Announcements" : None,
			"Events" : None,
			"Pictures" : None
		}
		db.child("clubs").push(clubname).set(dic)
		return render(request, "clubs/index.html",{"e":clubname})		
	return render(request,'clubs/addclub.html')

