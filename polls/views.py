# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Choice, Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


# def detail(request, question_id):
#     return HttpResponse("正在查看的是question:%s。" % question_id)

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("id为%s的Quetion不存在！" % question_id)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


# def results(request, question_id):
#     response = "查看question %s 的结果页面。"
#     return HttpResponse(response % question_id)
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


# def vote(request, question_id):
#     return HttpResponse("正在给question %s 投票！" % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {'question': question, 'error_message': "你还没有选择一个choice。"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 在成功处理POST的数据后返回一个HttpResponseRedirect。
        # 这可以避免当用户按下后退按钮时提交两次post
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))