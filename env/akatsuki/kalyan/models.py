from django.db import models
from django.utils import timezone
# Create your models here.

class Profile(models.Model):
    bcardid=models.CharField(max_length=50,unique=True)
    uname = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    
    # created_on = models.DateTimeField(default=timezone.now)
    # last_logged_in = models.DateTimeField(default=timezone.now)
    created_on = models.DateTimeField(auto_now_add=True)
    last_logged_in = models.DateTimeField(auto_now=True)
       
class Feedback(models.Model):
	uname = models.CharField(max_length=50)
	feed  = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	many_profile = models.ForeignKey(Profile)



class Category(models.Model):
	cname = models.CharField(max_length=50,unique=True)
	num_suggestions=models.IntegerField(default=0)
	num_complains=models.IntegerField(default=0)
	
class Suggestions(models.Model):
	uname = models.CharField(max_length=50)
	suggest_for=models.CharField(max_length=50)
	usuggestion= models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	many_profile = models.ForeignKey(Profile)
	many_category = models.ForeignKey(Category)
    


class Complains(models.Model):
	uname = models.CharField(max_length=50)
	complain_for=models.CharField(max_length=50)
	ucomplain = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	many_profile = models.ForeignKey(Profile)
	many_category = models.ForeignKey(Category)









