# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from google.oauth2 import service_account
import googleapiclient.discovery
# Create your views here.

import datetime

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
storage=firebase.storage()
user=3

import requests
from bs4 import BeautifulSoup
def convert(a):

	s = a.encode('ascii', 'ignore')
	return s
def createTT():
	soup = BeautifulSoup(open("/home/shubham/Desktop/xx.html"), 'html.parser')
	item = soup.find_all('td', attrs={'class': 'tabval'})

	data={}

	for i in range(0,len(item),8):
		#print item[i]
		dept = convert(item[i].text)
		prog = convert(item[i+1].text)[0]
		sem = convert(item[i+2].text)
		data["course"] = convert(item[i+3].text)
		data["room"] = convert(item[i+4].text)
		#print item[i+7].text
		if convert(item[i+7].text) == "N/A":
			data["slot"] = convert(item[i+6].text)
		else:
			#print "Hi "
			data["slot"] = convert(item[i+7].text)
		#sprint(data)
		db.child("TimeTable").child(dept).child(prog).child(sem).push(data)
		
# createTT()


def getemail():
	global user
	p="0"
	if user!=3:
		s=auth.get_account_info(user['idToken'])
		p = s['users'][0]['email']
	else:
		p="0"
	return p


def index(request):
	a=db.child('clubs').get()
	a=a.val()
	sed={}
	p=getemail()
	for r,t in a.items():
		sed[r]=t['pk']
	return render(request,'clubs/index.html',{"sed":sed,"email":p})

def signin(request):
	temp=db.child('clubs').get()
	temp=temp.val()
	sed={}
	for r,t in temp.items():
		sed[r]=t['pk']
	p=getemail()
	return render(request,'clubs/signin.html', {"email":p,"sed":sed})

def postsign(request):
	global user
	temp=db.child('clubs').get()
	temp=temp.val()
	sed={}
	for r,t in temp.items():
		sed[r]=t['pk']
	email=request.POST.get('email')
	passw = request.POST.get("pass")
	try:
		user = auth.sign_in_with_email_and_password(email,passw)
	except:
		message = "invalid cerediantials"
		p=getemail()
		return render(request,"clubs/signin.html",{"msg":message,"email":p})
	p=getemail()
	return render(request,'clubs/index.html',{"sed":sed,"email":p})

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
			"Pictures" : "None",	
			"pk" : l
		}
		db.child("clubs").child(clubname).set(dic)
		a=db.child('clubs').get()
		a=a.val()
		sed={}
		for r,t in a.items():
			sed[r]=t['pk']
		p=getemail()
		return render(request, "clubs/index.html",{"sed":sed,"email":p})	
	temp=db.child('clubs').get()
	temp=temp.val()
	sed={}
	for r,t in temp.items():
		sed[r]=t['pk']
	p=getemail()
	return render(request,'clubs/addclub.html', {"sed":sed,"email":p})

def displayclub(request,pk):
	temp=db.child('clubs').get()
	temp=temp.val()
	sed={}
	for r,t in temp.items():
		sed[r]=t['pk']
	all_clubs = db.child("clubs").get()
	a=all_clubs.val()
	for r,t in a.items():
		if t["pk"]==pk:
			ans=r
	p=getemail()
	return render(request,"clubs/displayclub.html",{"sed": sed, "pk":pk, "clubname":ans,"details":db.child("clubs").child(ans).get().val(),"email":p})

# def addpic(request,pk):


def desc(request,pk):
	temp=db.child('clubs').get()
	temp=temp.val()
	sed={}
	for r,t in temp.items():
		sed[r]=t['pk']
	if request.method == "POST":
		desc=request.POST.get('desc')
		all_clubs = db.child("clubs").get()
		a=all_clubs.val()
		for r,t in a.items():
			if t["pk"]==pk:
				ans=r
		db.child("clubs").child(ans).child("Desc").set(desc)
		p=getemail()
		return render(request,'clubs/displayclub.html',{"email":p,"sed": sed, "pk":pk, "clubname":ans,"details":db.child("clubs").child(ans).get().val()})	
	p=getemail()
	return render(request,'clubs/description.html', {"sed":sed, "pk":pk,"email":p})

def addannouncement(request,pk):
	temp=db.child('clubs').get()
	temp=temp.val()
	sed={}
	for r,t in temp.items():
		sed[r]=t['pk']
	if request.method == "POST":
		heading = request.POST.get('heading')
		announcement = request.POST.get('announcement')
		temp = (datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)).strftime('%d-%m-%Y %H:%M:%S')
		temp = temp.split(' ');
		date = temp[0]
		now = temp[1]
		all_clubs = db.child("clubs").get()
		a=all_clubs.val()
		for r,t in a.items():
			if t["pk"]==pk:
				ans=r
		ro={"heading":heading,"announcement":announcement,"date":str(date),"time":str(now)}
		db.child("clubs").child(ans).child("Announcements").push(ro)
		p=getemail()
		return render(request,'clubs/displayclub.html',{"email":p,"sed": sed, "pk": pk, "clubname":ans,"details":db.child("clubs").child(ans).get().val()})
	p=getemail()
	return render(request,'clubs/addannouncement.html', {"sed": sed, "pk": pk,"email":p})

def addevent(request,pk):
	temp=db.child('clubs').get()
	temp=temp.val()
	sed={}
	for r,t in temp.items():
		sed[r]=t['pk']
	if request.method == "POST":
		heading = request.POST.get('heading')
		description = request.POST.get('description')
		time = request.POST.get('time')
		date = request.POST.get('date')
		venue = request.POST.get('venue')
		mob = request.POST.get('mob')		
		all_clubs = db.child("clubs").get()
		a=all_clubs.val()
		for r,t in a.items():
			if t["pk"]==pk:
				ans=r
		ro = {"heading":heading,"description":description,"date":date,"time":time,"venue":venue,"mob":mob}
		db.child("clubs").child(ans).child("Events").push(ro)
		p=getemail()
		#addeventtocal(heading,description,date,time,venue,mob)
		return render(request,'clubs/displayclub.html',{"email":p,"sed": sed, "pk":pk, "clubname":ans,"details":db.child("clubs").child(ans).get().val()})
	p=getemail()
	return render(request,'clubs/addevent.html', {"sed": sed, "pk":pk,"email":p})




def addresource(request,pk):
	temp=db.child('clubs').get()
	temp=temp.val()
	sed={}
	for r,t in temp.items():
		sed[r]=t['pk']
	if request.method == "POST":
		heading = request.POST.get('heading')
		src = request.POST.get('src')	
		all_clubs = db.child("clubs").get()
		a=all_clubs.val()
		for r,t in a.items():
			if t["pk"]==pk:
				ans=r
		ro = {"heading":heading,"src":src}
		ann=db.child("clubs").child(ans).child("Res").push(ro)
		p=getemail()
		return render(request,'clubs/displayclub.html',{"email":p,"sed":sed, "pk":pk, "clubname":ans,"details":db.child("clubs").child(ans).get().val()})
	p=getemail()
	return render(request,'clubs/addresource.html', {"sed":sed, "pk":pk,"email":p})




def pic(request,pk):
	temp=db.child('clubs').get()
	temp=temp.val()
	sed={}
	for r,t in temp.items():
		sed[r]=t['pk']
	if request.method == "POST":
		#pic = request.POST.get('pic')
		
		print "HI"
		for filename, file in request.FILES.iteritems():
			name = request.FILES[filename].name
			uniq = datetime.datetime.now()
			name = name+"_"+ str(uniq)
			file_save=file
		t="images/"+name
		url=storage.child(t).get_url(1)
		storage.child(t).put(file_save)
		all_clubs = db.child("clubs").get()
		a=all_clubs.val()
		for r,t in a.items():
			if t["pk"]==pk:
				ans=r
		db.child("clubs").child(ans).child("Photo").set(url)
		p=getemail()
		return render(request,'clubs/displayclub.html',{"email":p,"sed":sed, "pk":pk,"clubname":ans,"details":db.child("clubs").child(ans).get().val()})
	p=getemail()
	return render(request,'clubs/getpic.html',{"sed":sed, "pk":pk,"email":p})




def pictures(request,pk):
	temp=db.child('clubs').get()
	temp=temp.val()
	sed={}
	for r,t in temp.items():
		sed[r]=t['pk']
	p=getemail()
	if request.method == "POST":
		#pic = request.POST.get('pic')
		lis = []
		print "HI"
		for file in request.FILES.getlist('pic'):
			name = file.name
			print name
			uniq = datetime.datetime.now()
			name = name+"_"+ str(uniq)
			file_save=file
			storage.child("images/"+name).put(file_save)
			lis.append(storage.child("images/"+name).get_url(1))

		all_clubs = db.child("clubs").get()
		a=all_clubs.val()
		for r,t in a.items():
			if t["pk"]==pk:
				ans=r

		for url in lis:
			db.child("clubs").child(ans).child("Pictures").push(url)
		return render(request,'clubs/displayclub.html',{"email":p,"sed":sed, "pk":pk,"clubname":ans,"details":db.child("clubs").child(ans).get().val()})
	return render(request,'clubs/getpictures.html',{"sed":sed, "pk":pk,"email":p})

def addeventtocal(heading, description, time, date, venue, mob):
	SCOPES = ['https://www.googleapis.com/auth/calendar']
	SERVICE_ACCOUNT_FILE = 'clubs/hackriti-110f1-f87a5e7af133.json'
	print date
	print time
	credentials = service_account.Credentials.from_service_account_file(
	        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
	adder=str(date)+"T"+str(time)+".000Z"
	print adder
	service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
	event = {
	  'summary': heading,
	  'location': venue,
	  'description': description,
	  'start': {
	    'dateTime': adder,
	    # 'timeZone': 'Asia/Kolkata',
	   },
	}

	event = service.events().insert(calendarId='iitghackriti@gmail.com', body=event).execute()
	print ('Event created: %s' % (event.get('htmlLink')))

def timetable(request):
	temp=db.child('clubs').get()
	temp=temp.val()
	sed={}
	for r,t in temp.items():
		sed[r]=t['pk']
	p=getemail()
	if request.method == "POST":
		branch=request.POST['branch']
		print branch
		prog=request.POST['program']
		print prog
		num=request.POST['semno']
		print num

		data=db.child("TimeTable").child(branch).child(prog).child(num).get().val()
		print "DONE READ!!"
		return render(request,'clubs/TimeTableForm.html',{"data":data,"sed":sed,"email":p})
	return render(request,'clubs/TimeTableForm.html',{"sed":sed,"email":p})

def events(request):
	temp=db.child('clubs').get()
	temp=temp.val()
	sed={}
	for r,t in temp.items():
		sed[r]=t['pk']

	p=getemail()
	return render(request, 'clubs/events.html',{"sed":sed,"email":p})