from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse(
        "<h1>首页</h1><br><a href='polls'>polls</a><br><a href='news'>news</a><br><a href='admin'>admin</a>")
