from django.urls import path
from . import views
urlpatterns = [
	path('home', views.index, name='polls_home_path')
]