from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
	# ex: /polls/
	path('', views.index, name='polls_index_path'),
	# ex: /polls/1
	path('<int:question_id>/', views.detail, name='polls_detail_path'),
	# ex: /polls/1/results
	path('<int:question_id>/results/', views.results, name='polls_results_path'),
	# ex: /polls/2/vote
	path('<int:question_id>/vote/', views.vote, name='polls_vote_path'),
	# ex: /polls/index/api
	path('index/api/', views.index_api, name='polls_index_api_path'),
]