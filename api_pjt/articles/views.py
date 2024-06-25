from django.shortcuts import render
from .models import Article


def article_list_html(request):
    articles = Article.objects.all()
    context = {'articles':articles}
    return render(request,'articles/article_list.html', context)