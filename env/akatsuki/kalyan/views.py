from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import *
from random import randint
from django.utils import timezone
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
import urllib.request, json 
		

def index(request):

	return render(request,"kalyan/HE/public/index.html",{})

def register(request):
	if("id" in request.session.keys()):
		return HttpResponseRedirect("/")
	flag = False
	aadharno = ''
	error = ''
	bah = ''
	if(request.method == 'POST'):
		bah = request.POST["bhamashah"]
		ada = request.POST["aadhar"]
		if(bah == '' or ada == ''):
			error = "All the fields are required"
		bah=bah.upper()
		string="https://apitest.sewadwaar.rajasthan.gov.in/app/live/Service/hofAndMember/ForApp/%s?client_id=ad7288a4-7764-436d-a727-783a977f1fe1" % (str(bah))	
		with urllib.request.urlopen(string) as url:
			data=json.loads(url.read().decode())
		if 'hof_Details' in data.keys():

			data=data['hof_Details']
			if 'AADHAR_ID' in data.keys():
	
			
				if str(data['AADHAR_ID'])==str(ada):
					flag=True
					
					request.session["prof"]=data
				else:
					error='Verification Failed, Check the entered FAMILY ID NO and Aadhar Id No and Try again..'
			else:
				error='Verification Failed, Check the entered FAMILY ID NO and Aadhar Id No and Try again..'
		else:
			error='Verification Failed, Check the entered FAMILY ID NO and Aadhar Id No and Try again..'


	# check with api if verified set flag = true else write into error 
	
	if(flag):
		request.session["aadhar"] = bah
		return HttpResponseRedirect("register/accept")
	if(error != '' and flag == False):
		return render(request,"kalyan/HE/public/register.html",{'error': error})
	return render(request,"kalyan/HE/public/register.html")





def accept(request):
	if("id" in request.session.keys()):
		return HttpResponseRedirect("/")
	if('aadhar' not in request.session.keys() and request.method == 'GET'):
		return HttpResponseRedirect("/")
	elif('aadhar' in request.session.keys() and request.method == 'GET'):
		return render(request,"kalyan/HE/public/accept.html")
	elif('aadhar'  in request.session.keys() and request.method == 'POST'):
		error = ''
		# request.session.pop("aadhar",None)
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
				# print(bah)
				profile_obj=Profile()
				profile_obj.bcardid=request.session["aadhar"]
				profile_obj.uname=username
				profile_obj.password=password
				profile_obj.save()
				obj=Profile.objects.filter(uname=username)
				# use this to get all rows in the table
				# qset=Profile.objects.all()
				# for i in qset:
				# 	print(i.uname,i.password,i.bcardid,timezone.localtime(i.created_on),timezone.localtime(i.last_logged_in))
				request.session["id"]=obj[0].bcardid
				
				if(request.POST["location"]==''):
					request.session["location"]="Location not known"
				else:
					request.session["location"]=request.POST["location"]	
				
				return HttpResponseRedirect("/login")
				# return render(request,"kalyan/HE/public/accept.html",{"error":"Registration Successful"})
		else:
			return render(request,"kalyan/HE/public/accept.html",{"error":error})


def login(request):
	if("id" in request.session.keys()):
		return HttpResponseRedirect("/")
	error=''
	if request.method=='POST':
		username = request.POST['username']
		password = request.POST['password']
		 
		obj=Profile.objects.filter(uname=username)
		if len(obj)==0:
			error='User not registered'
		else:
			if str(password) == str(obj[0].password):
				request.session["id"]=obj[0].bcardid
				error='Login Successful'
				# if obj[0].user_type==False:
				# 	string="https://apitest.sewadwaar.rajasthan.gov.in/app/live/Service/hofAndMember/ForApp/%s?client_id=ad7288a4-7764-436d-a727-783a977f1fe1" % (str(obj[0].bcardid))	
				# 	with urllib.request.urlopen(string) as url:
				# 		data=json.loads(url.read().decode())
				# 	data=data['hof_Details']
				# 	request.session["prof"]=data
				if(request.POST["location"]==''):
					request.session["location"]="Location not known"
				else:
					request.session["location"]=request.POST["location"]
				if obj[0].user_type:
					request.session["gov"]=True
				return HttpResponseRedirect("/")

			else:
				error='Wrong Password'
	return render(request,"kalyan/HE/public/login.html",{"error":error})

def about(request):
	return render(request,"kalyan/HE/public/about.html",{})

def feedback(request):
	# database error
	if("id" not in request.session.keys()):
		print("-------")
		return HttpResponseRedirect("/register")
	if(request.method=="POST"):
		feed=str(request.POST['description'])
		if len(re.findall('[a-zA-Z]',feed))==0:
			a='Please enter some text to give the feedback'
			return render(request,"kalyan/HE/public/feedback.html",{"a":a,"color":"red"})
		fobj=Feedback()
		feed_text = request.POST['description']
		obj=Profile.objects.filter(pk=request.session["id"])
		fobj.uname=obj[0].uname
		fobj.feed=feed_text
		fobj.save()
		return render(request,"kalyan/HE/public/feedback.html",{"a":"Feedback Submitted","color":"green"})
	else:
		return render(request,"kalyan/HE/public/feedback.html",{})


ls = []
def scomplain(request):
	ls = []
	sub=''
	#SUBJECT 
	cqset=Category.objects.all()
	for i in cqset:
		ls.append(i.cname)
	if(request.method == 'POST' and 'lsubmit' in request.POST.keys()):
		return HttpResponseRedirect("login")
	# if(request.method == 'POST' and 'complain' in request.POST.keys() and 'dropdown' in request.POST.keys()):
	# 	option_val=request.POST['dropdown']
	suggest_text = ''
	if(request.method == 'POST'):
		suggest_text=str(request.POST['description'])
		if len(re.findall('[a-zA-Z]',suggest_text))==0:
			a='Please enter some text to give the suggestion'
			return render(request,"kalyan/HE/public/scomplain.html",{"a":a,"color":"red","list":ls})
		if len(re.findall('[a-zA-Z]',str(request.POST['subject'])))==0:
			a='Write a subject'
			sub = str(request.POST['subject'])
			return render(request,"kalyan/HE/public/scomplain.html",{"a":a,"color":"red","list":ls})

	if(request.method == 'POST' and 'complain' in request.POST.keys()):
		print("write database into complain fields")
		complain_text=suggest_text
		obj=Profile.objects.filter(bcardid=request.session["id"])
		cur_uname=obj[0].uname
		complainfor=request.POST["dropdown"]
		cobj=Complains()
		cobj.uname=cur_uname
		cobj.subject=request.POST["subject"]
		cobj.ucomplain=complain_text
		cobj.complain_for=complainfor
		cobj.ulocation=request.session["location"]
		cobj.save()
		# obj = Category.objects.get(cname=complainfor)
		# obj.num_complains=obj.num_complains+1
		# obj.save()



		a = 'complain filed'
		return HttpResponseRedirect("/public_views/complains/all")
		# return render(request,"kalyan/HE/public/scomplain.html",{"a":a,"color":"green","list":ls})
	
	elif(request.method == 'POST' and 'suggest' in request.POST.keys()):
		print("write database into suggest field")
		suggest_text=str(request.POST['description'])
		obj=Profile.objects.filter(bcardid=request.session["id"])
		cur_uname=obj[0].uname
		suggestfor=request.POST["dropdown"]
		sobj=Suggestions()
		sobj.uname=cur_uname
		sobj.subject=request.POST["subject"]

		sobj.usuggestion=suggest_text
		sobj.suggest_for=suggestfor
		sobj.save()
		# obj = Category.objects.get(cname=suggestfor)
		# obj.num_suggestions=obj.num_suggestions+1
		# obj.save()


		a = 'suggestion registered'
		return HttpResponseRedirect("/public_views/suggestions/all")
		
		# return render(request,"kalyan/HE/public/scomplain.html",{"a":a,"color":"green","list":ls})
	
	else:
		return render(request,"kalyan/HE/public/scomplain.html",{"list":ls,"a":"Don't disclose your identity when writing into the box.","color":"purple"})




def public_views(request,vtype=None,ctype=None):
	cat=ctype.replace("_"," ")
	if vtype=='complains':
		if cat=="all":
			comqset_list=Complains.objects.all()
		else:
			comqset_list=Complains.objects.filter(complain_for=cat)

		

		topic="Complains"
		refer="Filed against"
		side_topic="Suggestions"
		val='suggestions'
		
	elif vtype=='suggestions':
		if cat=="all":
			comqset_list=Suggestions.objects.all()
		else:
			comqset_list=Suggestions.objects.filter(suggest_for=cat)


		topic="Suggestions"
		refer="Suggestion for"
		side_topic="Complains"
		val='complains'
		
	paginator = Paginator(comqset_list, 5) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		comqset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		comqset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		comqset = paginator.page(paginator.num_pages)

	# all_sug=Category.objects.all().aggregate(Sum('num_suggestions')).get('num_suggestions__sum', 0)

	# all_comp=Category.objects.all().aggregate(Sum('num_complains')).get('num_complains__sum', 0)
	all_sug=Suggestions.objects.all().count()
	all_comp=Complains.objects.all().count()
	catqset=Category.objects.all()
	ls=[]
	for obj in catqset:
		numcomp=Complains.objects.filter(complain_for=obj.cname).count()
		numsugg=Suggestions.objects.filter(suggest_for=obj.cname).count()
		ls.append([numcomp,numsugg,obj.cname])
			
	
	context={	"comqset":comqset,
				"catqset":catqset,
				"refer":refer,
				"topic":topic,
				"side_topic":side_topic,
				"val":val,
				"all_sug":all_sug,
				"all_comp":all_comp,
				"cval":ctype,
				"antival":vtype,
				"cat":cat,
				"ls":ls
			}
	return render(request,"kalyan/HE/public/public_views.html",context)



def public_view_detail(request,vtype=None,id=None):
	if("id" not in request.session.keys()):
		return HttpResponseRedirect("/public_views/complains/all/")

	if vtype=='complains':
		instance=get_object_or_404(Complains,id=id)
		refer="Filed against"
		cvar="Complain filing location :"
	
	elif vtype=='suggestions':
		instance=get_object_or_404(Suggestions,id=id)
		refer="Suggestion for"
		cvar=""

	obj=Profile.objects.filter(bcardid=request.session["id"])
	utype=obj[0].user_type
	if utype==True:
		pobj=Profile.objects.filter(uname=instance.uname)
		request.session["userprof"]=pobj[0].bcardid

			
	else:
		pobj=''
		

	context={
				"instance":instance,
				"refer":refer,
				"pobj":pobj,
				"flag":utype,
				"cvar":cvar

			}	
	return render(request,"kalyan/HE/public/public_view_detail.html",context)

def service(request,id=None):
	
	aobj=AppCategory.objects.all()
	obj={}
			
	if int(id)>0:
		obj[id]=True
		pqbj=Profile.objects.filter(bcardid=request.session["id"])
		cur_uname=pqbj[0].uname
		myobj=Applications()
		myobj.uname=cur_uname
		myobj.app_name=aobj[int(id)-1].app_name
		myobj.save()

	return render(request,"kalyan/HE/public/avail.html",{"obj":obj,"aobj":aobj})
	
	


def logout(request):
	request.session.pop("id",None)
	request.session.pop("gov",None)
	request.session.pop("location",None)
	request.session.pop("prof",None)
	request.session.pop("aadhar",None)

	return render(request,"kalyan/HE/public/index.html",{})




def profile(request,vtype=None):
	# d64={}
	# if('prof' in request.session.keys()):
	# 	data=request.session["prof"]
	# else:
	# 	data = ''
	# string="https://apitest.sewadwaar.rajasthan.gov.in/app/live/Service/hofMembphoto/%s/%s?client_id=ad7288a4-7764-436d-a727-783a977f1fe1" % (str(data['BHAMASHAH_ID']),str(data['M_ID']))	
	# with urllib.request.urlopen(string) as url:
	# 	d64=json.loads(url.read().decode())
	# context={

	# 	"data":data,
	# 	"d64":d64["hof_Photo"]["PHOTO"]
	# }

	# print(data)


	# return render(request,"kalyan/HE/public/profile_page.html",context)	

	string="https://apitest.sewadwaar.rajasthan.gov.in/app/live/Service/hofAndMember/ForApp/%s?client_id=ad7288a4-7764-436d-a727-783a977f1fe1" % (str(vtype))	
	with urllib.request.urlopen(string) as url:
		data=json.loads(url.read().decode())
	data=data['hof_Details']


	string="https://apitest.sewadwaar.rajasthan.gov.in/app/live/Service/hofMembphoto/%s/%s?client_id=ad7288a4-7764-436d-a727-783a977f1fe1" % (str(data['BHAMASHAH_ID']),str(data['M_ID']))	
	with urllib.request.urlopen(string) as url:
		d64=json.loads(url.read().decode())

	context={

		"data":data,
		"d64":d64["hof_Photo"]["PHOTO"]

	}

	print(data)

	return render(request,"kalyan/HE/public/profile_page.html",context)	






# def view_user(request,vtype=None,id=None):
	
# 	string="https://apitest.sewadwaar.rajasthan.gov.in/app/live/Service/hofAndMember/ForApp/%s?client_id=ad7288a4-7764-436d-a727-783a977f1fe1" % (str(request.session["userprof"]))	
# 	with urllib.request.urlopen(string) as url:
# 		data=json.loads(url.read().decode())
# 	data=data['hof_Details']
# 	request.session.pop("userprof",None)			


# 	string="https://apitest.sewadwaar.rajasthan.gov.in/app/live/Service/hofMembphoto/%s/%s?client_id=ad7288a4-7764-436d-a727-783a977f1fe1" % (str(data['BHAMASHAH_ID']),str(data['M_ID']))	
# 	with urllib.request.urlopen(string) as url:
# 		d64=json.loads(url.read().decode())

# 	context={

# 		"data":data,
# 		"d64":d64["hof_Photo"]["PHOTO"]

# 	}

# 	print(data)


# 	return render(request,"kalyan/HE/public/user_profile_request.html",context)	



def app_view(request):
	ls=[]
	qset=Applications.objects.all()
	for obj in qset:
		imo=Profile.objects.filter(uname=obj.uname)
		ls.append([obj.app_name,obj.uname,imo[0].bcardid,obj.created_on])
	return render(request,"kalyan/HE/public/application_views.html",{"ls":ls,"flag":False})	


	
		
	
	