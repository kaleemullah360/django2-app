from django.shortcuts import render
from django.http import HttpResponse
from django.template.defaultfilters import pprint
import json
from django.core import serializers
# Create your views here.

def index(request):
	return HttpResponse(pprint(dir(request)), content_type='application/json') 