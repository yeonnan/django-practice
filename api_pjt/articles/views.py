from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer


def article_list_html(request):
    articles = Article.objects.all()
    context = {'articles':articles}
    return render(request,'articles/article_list.html', context)


def json_01(request):
    articles = Article.objects.all()
    json_articles = []

    for article in articles:
        json_articles.append(
            {
            'title':article.title,
            'content':article.content,
            'created_at':article.created_at,
            'updated_at':article.updated_at,
            }
        )
    # safe : json_articles에 들어간게 dict이면 safe=False를 안적어줘도 된다.
    # 지금은 [], list가 들어있기 때문에 safe=False로 적어주면 내부적으로 처리해서 JsonResponse를 돌려준다.
    return JsonResponse(json_articles, safe=False)  


def json_02(request):
    articles = Article.objects.all()
    # jsno 포맷으로, articles 데이터로 직렬화
    res_data = serializers.serialize('json', articles)
    # content_type : Response 구조 중에 정보로 들어있다.
    return HttpResponse(res_data, content_type='application/json')


@ api_view(['GET'])
def json_drf(request):
    # 1. 데이터를 다 가져온 후
    articles = Article.objects.all()
    # 2. 정의해둔 ArticleSerializer를 기져온다.
    # 조회한 queryset(articles)을 그대로 넣어주는데, queryset이 단일 객체이면 many=True를 빼둬된다.
    # 지금은 all -> 여러개이기 때문에 many=True를 넣어줘야 한다.
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)