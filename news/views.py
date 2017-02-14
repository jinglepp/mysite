from django.shortcuts import render

# Create your views here.
from .models import Article
from datetime import date


def year_archive(request, year):
    a_list = Article.objects.filter(pub_date__year=year)
    context = {'year': year, 'article_list': a_list}
    return render(request, 'news/year_archive.html', context)


def month_archive(request, year, month):
    return None


def article_detail(request, ):
    return None


def news_index(request):
    year = date.today().year
    return year_archive(request, year)
