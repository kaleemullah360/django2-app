from django.contrib import admin
from weblog import models
# Register your models here.
admin.site.register(
	({
		models.Blog, models.Author, models.Entry
		})
	)