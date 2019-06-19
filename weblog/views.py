from django.shortcuts import render
from weblog.models import Author, Blog, Entry
# Create your views here.

def index(request):
	return Author.objects.all()