from django.contrib import admin
from django.urls import path, include
from . import models
# Register your models here.

admin.site.register(
	(
		{
		models.Question, models.Choice
		}
	))