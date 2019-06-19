from django.urls import path, include
from weblog import views
urlpatterns = [
	path('blog/', views.index, name="weblog_blog_path")
]