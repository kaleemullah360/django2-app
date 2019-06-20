from django.shortcuts import render
from django.utils import timezone
from django.http.response import JsonResponse
from weblog.models import Author, Blog, Entry
# Create your views here.

def index_api(request):
	json_r = build_index_api_data(request)
	return JsonResponse(json_r)

def build_index_api_data(request):
	all_authors = Author.objects.all()
	json_r = {}
	if all_authors.count() > 0:
		json_r['status']= '1'
		json_r['timestamp']= timezone.now()
		json_r['message'] = '%d records found' % (all_authors.count())
		json_r['response']= list(all_authors.values())
	else:
		json_r['status']= '0'
		json_r['timestamp']= timezone.now()
		json_r['message'] = '%d records found' % (all_authors.count())
		json_r['response']= []

	return json_r