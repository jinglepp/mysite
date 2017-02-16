from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import Question

# # 使用HttpResponse
# def index(request):
#     # return HttpResponse("你好，这是polls的索引页！")
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # output = ", ".join([q.question_text for q in latest_question_list])
#     output = ", <BR>".join([q.question_text + ' - ' + q.pub_date.strftime("%Y年%m月%d日") for q in latest_question_list])
#     return HttpResponse(output)

# # 使用loader
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {'latest_question_list': latest_question_list}
#     return HttpResponse(template.render(context, request))

# 使用快捷方式render()
from django.shortcuts import render


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    return HttpResponse("正在查看的是question:%s。" % question_id)


def results(request, question_id):
    response = "查看question %s 的结果页面。"
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("正在给question %s 投票！" % question_id)
