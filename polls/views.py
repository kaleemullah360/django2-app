from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.utils import timezone
from polls.models import Choice, Question  # Import the model classes we just 
# Create your views here.

def index(request):
	json_r = build_index_data(request)
	return JsonResponse(json_r)

def index_api(request):
	json_r = build_index_data(request)
	return JsonResponse(json_r)

def build_index_data(request):
	questions = Question.objects.filter(question_text__contains="new", pub_date__lte=timezone.now())
	q_1 = Question.objects.filter(id=1)
	q_1 = q_1.first()
	q_1_c=q_1.choice_set.create(choice_text='Not listed', votes=0)
	q_1 = q_1.choice_set.all()
	q_1_c.delete()

	current_year = timezone.now().year
	questions.filter(pub_date__year=current_year)
	json_r = {}
	if questions.count() > 0:
		json_r['status']= '1'
		json_r['timestamp']= timezone.now()
		json_r['response']= list(questions.values())
		json_r['choices']= list(q_1.values())
		json_r['message'] = '%d records found' % (questions.count())
	else:
		json_r['status']= '0'
		json_r['timestamp']= timezone.now()
		json_r['response']= []
		json_r['choices']= []
		json_r['message'] = '%d records found' % (questions.count())
	return json_r
