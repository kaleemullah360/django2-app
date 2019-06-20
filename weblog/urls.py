from django.urls import path, include
from weblog import views
urlpatterns = [
	path('index/api', views.index_api, name="weblog_index_api_path")
]