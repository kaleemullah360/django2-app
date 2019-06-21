from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.http.response import JsonResponse
from django.utils import timezone
from django.urls import reverse
from polls.models import Choice, Question  # Import the model classes we just 
from django.views import generic
from django.db.models import F
# Create your views here.
notfound_template = loader.get_template('http_404.html')
notfound_template_path = 'http_404.html'


class IndexView(generic.ListView):
	template_name = 'polls/index_list_view.html'
	context_object_name = 'latest_q'

	def get_queryset(self):
		"""Return the last five published questions."""
		return Question.objects.order_by('-pub_date')[:5]

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results_detail_view.html'

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail_detail_view.html'

def index(request):
	template = loader.get_template('polls/index.html')
	template_path = 'polls/index.html'
	latest_q = Question.objects.order_by('-pub_date')[:5]
	#latest_q = list(latest_q.values())
	context_dict = {
		'latest_q': latest_q,
	}
	#latest_q = ", ".join([q.question_text for q in latest_q])
	html_data = template.render(context_dict, request)
	#return HttpResponse(html_data) # for sending html response 
	return render(request, template_path, context_dict) # alternative method for sending html response 

def detail(request, question_id):
	template = loader.get_template('polls/detail.html')
	template_path = 'polls/detail.html'
	context_dict = {}
	
	question = get_object_or_404(Question, pk=question_id)
	context_dict['question'] = question
	return render(request, template_path, context_dict)

	try:
		question = Question.objects.get(pk=question_id)
		context_dict['question'] = question
		html_data = template.render(context_dict, request)
	except Question.DoesNotExist:
		html_data = notfound_template.render(context_dict, request)
		raise Http404(html_data)
	#return HttpResponse(html_data)
	return render(request, template_path, context_dict)


def results(request, question_id):
	template = loader.get_template('polls/results.html')
	template_path = 'polls/results.html'
	context_dict = {}
	question = get_object_or_404(Question, pk=question_id)
	try:
		# do somthing
		context_dict['question'] = question
		question.choice_set.all()
	except (KeyError, Question.DoesNotExist):
		# if fails then respond
		return Http404('Something went wrong')
	else:
		# do something else
		question.choice_set.all()
	response = "You're looking at the results of question %s."
	return render(request, template_path, context_dict)

def vote(request, question_id):
	#template = loader.get_template('polls/vote.html')
	detail_template = loader.get_template('polls/detail.html')
	#template_path = 'polls/vote.html'
	detail_template_path = 'polls/detail.html'
	context_dict = {}

	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# request.POST['choice'] will raise KeyError if choice wasn’t provided in POST data. 
		# The above code checks for KeyError and redisplays the question form with an error message if choice isn’t given.
		# redisplay the question voting form
		context_dict = {
			'question': question,
			'error_message': "You didn't select a choice."
		}
		return render(request, detail_template_path, context_dict)
	else:
		# this block will not caught by exception when exception is raised
		# F() objects assigned to model fields persist after saving the model instance and will be applied on each save(). For example:
		# F() is used to avoid race condition
		selected_choice.votes = F('votes') + 1
		selected_choice.save()
		# Be sure to refresh it if you need to access the field.
		selected_choice.refresh_from_db()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.

	return HttpResponseRedirect(reverse('polls:polls_results_path', args=(question.id,)))

def index_api(request):
	json_r = build_index_api_data(request)
	return JsonResponse(json_r)

def build_index_api_data(request):
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
