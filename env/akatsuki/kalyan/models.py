from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
# Create your models here.

class Profile(models.Model):
    bcardid=models.CharField(max_length=50,unique=True,verbose_name="ID")
    uname = models.CharField(max_length=50,unique=True,verbose_name="User Name")
    password = models.CharField(max_length=50)
    user_type=models.BooleanField(default=False,verbose_name="Government Official")
    # A -> admin G -> govt_official P -> Public 
    # can you please make this boolean since we don't need admin
    
    # created_on = models.DateTimeField(default=timezone.now)
    # last_logged_in = models.DateTimeField(default=timezone.now)
    created_on = models.DateTimeField(auto_now_add=True,verbose_name="Created On")
    last_logged_in = models.DateTimeField(auto_now=True,verbose_name="Last Login Time")
	


       
class Feedback(models.Model):
	uname = models.CharField(max_length=50,verbose_name="User Name")
	feed  = models.TextField(max_length=500,verbose_name="Feedback")
	created_on = models.DateTimeField(auto_now_add=True,verbose_name="Feedback")
	# many_profile = models.ForeignKey(Profile)



class Category(models.Model):
	cname = models.CharField(max_length=50,unique=True,verbose_name="Category")
	# num_suggestions=models.IntegerField(default=0)
	# num_complains=models.IntegerField(default=0)
	class Meta:
		verbose_name = "Category"
		verbose_name_plural = "Categories"
	# def get_absolute_url(self):
	# 	return reverse("kalyan:kalyan_public_views",kwargs={"vtype":'complains',"ctype":self.cname.replace(" ","_")})


	
class Suggestions(models.Model):
	uname = models.CharField(max_length=50,verbose_name="User Name")
	suggest_for=models.CharField(max_length=50,verbose_name="Suggestion For")
	subject=models.CharField(max_length=30,default='Suggestion',verbose_name="Subject")
	usuggestion= models.TextField(max_length=500,verbose_name="Suggestion")
	created_on = models.DateTimeField(auto_now_add=True,verbose_name="Created On")
	# many_profile = models.ForeignKey(Profile)
	# many_category = models.ForeignKey(Category)

	def get_absolute_url(self):
		return reverse("kalyan:kalyan_public_view_detail",kwargs={"vtype":'suggestions',"id":self.id})


	class Meta:
		ordering=["-created_on"]
		verbose_name = "Suggestion"
		verbose_name_plural = "Suggestions"
    


class Complains(models.Model):
	uname = models.CharField(max_length=50,verbose_name="User Name")
	complain_for=models.CharField(max_length=50,verbose_name="Complain For")
	subject=models.CharField(max_length=100,default='Complain',verbose_name="Subject")
	ucomplain = models.TextField(max_length=500,verbose_name="Complain")
	created_on = models.DateTimeField(auto_now_add=True,verbose_name="Created On")
	ulocation=models.CharField(max_length=200,default='Location Not known')
	# many_profile = models.ForeignKey(Profile)
	# many_category = models.ForeignKey(Category)
	
	def get_absolute_url(self):
		return reverse("kalyan:kalyan_public_view_detail",kwargs={"vtype":'complains',"id":self.id})


	class Meta:
		ordering=["-created_on"]
		verbose_name = "Complain"
		verbose_name_plural = "Complains"


class AppCategory(models.Model):
	app_name=models.CharField(max_length=100,default='Application',verbose_name="Application name")
	app_desc=models.TextField(max_length=500,verbose_name="Application Description")
	class Meta:
		verbose_name = "AppCategory"
		verbose_name_plural = "AppCategory"
	


class Applications(models.Model):
	uname=models.CharField(max_length=50,verbose_name="User name")
	app_name=models.CharField(max_length=50,default='application',verbose_name="Application Name")
	created_on=models.DateTimeField(auto_now_add=True,verbose_name="Created On")
	class Meta:
		ordering=["created_on"]
		verbose_name = "Application"
		verbose_name_plural = "Applications"
	








