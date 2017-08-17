from django.contrib import admin
from django.utils.translation import ugettext_lazy
from django.contrib.admin import AdminSite
from .models import *

# class MyAdminSite(AdminSite):
# 	site_title = ugettext_lazy('Kalyan Yojana')
# 	site_header = ugettext_lazy('Administration')
# 	index_title = ugettext_lazy('Kalyan Yojana')

# admin_site = MyAdminSite()

class CategoryA(admin.ModelAdmin):
	exclude = ('num_suggestions','num_complains')
	list_display = ['cname']
	ordering = ['cname']

class ProfileA(admin.ModelAdmin):
	list_display = ['bcardid','uname','password','user_type']
	ordering = ['bcardid']

class SuggestionsA(admin.ModelAdmin):
	list_display = ['uname','subject','suggest_for','created_on']
	ordering = ['created_on']
	exclude = ('created_on',)

class ComplainsA(admin.ModelAdmin):
	list_display = ['uname','subject','complain_for','created_on']
	ordering = ['created_on']
	exclude = ('created_on',)

class FeedbackA(admin.ModelAdmin):
	list_display = ['uname','feed','created_on']
	ordering = ['created_on']
	exclude = ('created_on',)

admin.site.register(Profile,ProfileA)
admin.site.register(Category,CategoryA)
admin.site.register(Suggestions,SuggestionsA)
admin.site.register(Complains,ComplainsA)
admin.site.register(Feedback,FeedbackA)
admin.site.register(Applications)
admin.site.register(AppCategory)

# Register your models here.
