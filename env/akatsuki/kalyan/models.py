from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
# Create your models here.

class Profile(models.Model):
    bcardid=models.CharField(max_length=50,unique=True)
    uname = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    user_type=models.BooleanField(default=False)
    # A -> admin G -> govt_official P -> Public 
    
    # created_on = models.DateTimeField(default=timezone.now)
    # last_logged_in = models.DateTimeField(default=timezone.now)
    created_on = models.DateTimeField(auto_now_add=True)
    last_logged_in = models.DateTimeField(auto_now=True)
       
class Feedback(models.Model):
	uname = models.CharField(max_length=50)
	feed  = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	# many_profile = models.ForeignKey(Profile)



class Category(models.Model):
	cname = models.CharField(max_length=50,unique=True)
	num_suggestions=models.IntegerField(default=0)
	num_complains=models.IntegerField(default=0)
	# def get_absolute_url(self):
	# 	return reverse("kalyan:kalyan_public_views",kwargs={"vtype":'complains',"ctype":self.cname.replace(" ","_")})

	
class Suggestions(models.Model):
	uname = models.CharField(max_length=50)
	suggest_for=models.CharField(max_length=50)
	subject=models.CharField(max_length=100,default='Suggestion')
	usuggestion= models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	# many_profile = models.ForeignKey(Profile)
	# many_category = models.ForeignKey(Category)

	def get_absolute_url(self):
		return reverse("kalyan:kalyan_public_view_detail",kwargs={"vtype":'suggestions',"id":self.id})


	class Meta:
		ordering=["-created_on"]
    


class Complains(models.Model):
	uname = models.CharField(max_length=50)
	complain_for=models.CharField(max_length=50)
	subject=models.CharField(max_length=100,default='Complain')
	ucomplain = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	# many_profile = models.ForeignKey(Profile)
	# many_category = models.ForeignKey(Category)
	
	def get_absolute_url(self):
		return reverse("kalyan:kalyan_public_view_detail",kwargs={"vtype":'complains',"id":self.id})


	class Meta:
		ordering=["-created_on"]










