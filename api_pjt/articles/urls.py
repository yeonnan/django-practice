from django.urls import path
from . import views

app_mname = 'articles'
urlpatterns = [
    path('html/', views.article_list_html, name='article_list_html'),
    path('json-01/', views.json_01, name='json_01'),
]