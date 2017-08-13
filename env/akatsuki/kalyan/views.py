from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import *
from random import randint
from django.utils import timezone
import re

aadhar = ''
bah=''
def index(request):
	return render(request,"kalyan/HE/public/index.html",{})

def register(request):
	flag = True
	aadharno = 0
	error = ''
	if(request.method == 'POST'):
		bah = request.POST["bhamashah"]
		ada = request.POST["aadhar"]
		if(bah == '' or ada == ''):
			error = "All the fields are required"
	# check with api if verified set flag = true else write into error 
	
	if(flag):
		request.session["aadhar"] = aadharno
		return HttpResponseRedirect("register/accept")
	if(error != '' and flag == False):
		return render(request,"kalyan/HE/public/register.html",{'error': error})
	return render(request,"kalyan/HE/public/register.html")

def accept(request):
	if('aadhar' not in request.session.keys() and request.method == 'GET'):
		return HttpResponseRedirect("/")
	elif('aadhar' in request.session.keys() and request.method == 'GET'):
		aadhar = request.session["aadhar"]
		request.session.pop("aadhar",None)
		return render(request,"kalyan/HE/public/accept.html")
	elif('aadhar' not in request.session.keys() and request.method == 'POST'):
		request.session.pop("aadhar",None)
		error = ''
		username = request.POST['username']
		password = request.POST['password']


		confirmation = request.POST['confirmation']
		if(username == '' or password == '' or confirmation == ''):
			error = "All the fields are required"
		elif(password != confirmation):
			error = "Password did not match..."
		if(error == ''):
			obj=Profile.objects.filter(uname=username)
			if len(obj)>0:
				error='Username already exists'
				return render(request,"kalyan/HE/public/accept.html",{"error":error})
	

			else:
				profile_obj=Profile()
				bah=str(randint(0,5000))
				profile_obj.bcardid=bah
				profile_obj.uname=username
				profile_obj.password=password
				profile_obj.save()
				obj=Profile.objects.filter(uname=username)
				# use this to get all rows in the table
				# qset=Profile.objects.all()
				# for i in qset:
				# 	print(i.uname,i.password,i.bcardid,timezone.localtime(i.created_on),timezone.localtime(i.last_logged_in))
				request.session["id"]=obj[0].pk
				return render(request,"kalyan/HE/public/accept.html",{"error":"Registration Successful"})
		else:
			return render(request,"kalyan/HE/public/accept.html",{"error":error})


def login(request):
	error=''
	if request.method=='POST':
		username = request.POST['username']
		password = request.POST['password']
		 
		obj=Profile.objects.filter(uname=username)
		if len(obj)==0:
			error='User not registered'
		else:
			if str(password) == str(obj[0].password):
				request.session["id"]=obj[0].pk
				error='Login Successful'
			else:
				error='Wrong Password'
	return render(request,"kalyan/HE/public/login.html",{"error":error})

def about(request):
	return render(request,"kalyan/HE/public/about.html",{})

def feedback(request):
	# if(request.method=="POST"):
	# 	if "id" in request.session.keys():
	# 		fobj=Feedback()
	# 		feed_text = request.POST['description']
	# 		obj=Profile.objects.filter(pk=request.session["id"])
	# 		fobj.uname=obj[0].uname
	# 		fobj.feed=feed_text
	# 		fobj.save()
	# 		qset=Feedback.objects.all()
	# 		for i in qset:
	# 			print(i.uname,i.feed,timezone.localtime(i.created_on))
	# else:
	# 	return render(request,"kalyan/HE/public/feedback.html",{})
	# else:
		return HttpResponseRedirect("register")



def scomplain(request):
	if(request.method == 'POST' and 'lsubmit' in request.POST.keys()):
		return HttpResponseRedirect("login")
	# if(request.method == 'POST' and 'complain' in request.POST.keys() and 'dropdown' in request.POST.keys()):
	# 	option_val=request.POST['dropdown']

	if(request.method == 'POST' and 'csubmit' in request.POST.keys() and 'description' in request.POST.keys()):
		print("write database into complain fields")
		complain_text=str(request.POST['description'])
		
		obj=Profile.objects.filter(pk=request.session["id"])
		cur_uname=obj[0].uname
		cobj=Complains()
		cobj.uname=cur_uname
		cobj.ucomplain=complain_text
		cobj.complain_for="helo"
		cobj.save()

		a = 'complain filed'
		return render(request,"kalyan/HE/public/scomplain.html",{"a":a})
	elif(request.method == 'POST' and 'ssubmit' in request.POST.keys() and 'description' in request.POST.keys()):
		print("write database into suggest field")
		suggest_text=str(request.POST['description'])
		if len(re.findall('[a-zA-Z]',suggest_text))==0:
			a='Please enter some text to give the suggestion'
		else:
			obj=Profile.objects.filter(pk=request.session["id"])
			cur_uname=obj[0].uname
			sobj=Suggestions()
			sobj.uname=cur_uname
			sobj.usuggestion=suggest_text
			# sobj.suggest_for=option_val
			sobj.save()
			a = 'suggestion registered'
		return render(request,"kalyan/HE/public/scomplain.html",{"a":a})
	
	else:
		ls = []
		cqset=Category.objects.all()
		for i in cqset:
			ls.append(i.cname)
		return render(request,"kalyan/HE/public/scomplain.html",{"list":ls})




def public_views(request):
	ls=[]
	qset=Complains.objects.all()
	for obj in qset:
		ls.append([obj.uname,obj.complain_for,obj.ucomplain,timezone.localtime(obj.created_on)])

	return render(request,"kalyan/HE/public/public_views.html",{"ls":ls})



def logout(request):
	request.session.pop("id",None)
	return render(request,"kalyan/HE/public/index.html",{})