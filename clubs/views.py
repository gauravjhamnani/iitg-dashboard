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
	a=db.child('clubs').get()
	a=a.val()
	sed={}
	for r,t in a.items():
		sed[r]=t['pk']
	return render(request,'clubs/index.html',{"sed":sed})

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
	a=db.child('clubs').get()
	a=a.val()
	sed={}
	for r,t in a.items():
		sed[r]=t['pk']
	return render(request,'clubs/index.html',{"sed":sed})

def addclub(request):
	if request.method == "POST":
		clubname = request.POST.get('clubname')
		email = request.POST.get('email')
		password = request.POST.get('password')
		auth.create_user_with_email_and_password(email, password)
		l=clubname.split(' ')
		l=l[0].lower()
		dic={
			"email" : email,
			"Photo": "None",
			"Desc" : "None",
			"Res" : "None",
			"Announcements" : "None",
			"Events" : "None",
			"Pictures" : "None",	
			"pk" : l
		}
		db.child("clubs").child(clubname).set(dic)
		a=db.child('clubs').get()
		a=a.val()
		sed={}
		for r,t in a.items():
			sed[r]=t['pk']
		return render(request, "clubs/index.html",{"sed":sed})		
	return render(request,'clubs/addclub.html')

def displayclub(request,pk):
	all_clubs = db.child("clubs").get()
	a=all_clubs.val()
	for r,t in a.items():
		if t["pk"]==pk:
			ans=r
	return render(request,"clubs/displayclub.html",{"clubname":ans,"details":db.child("clubs").child(ans).get().val()})
