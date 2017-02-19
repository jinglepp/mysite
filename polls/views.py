# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Choice, Question
from django.views import generic

from django.utils import timezone


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)
#
#
# # def detail(request, question_id):
# #     return HttpResponse("正在查看的是question:%s。" % question_id)
#
# # def detail(request, question_id):
# #     try:
# #         question = Question.objects.get(pk=question_id)
# #     except Question.DoesNotExist:
# #         raise Http404("id为%s的Quetion不存在！" % question_id)
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
#
# # def results(request, question_id):
# #     response = "查看question %s 的结果页面。"
# #     return HttpResponse(response % question_id)
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
#
#
# # def vote(request, question_id):
# #     return HttpResponse("正在给question %s 投票！" % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {'question': question, 'error_message': "你还没有选择一个choice。"})
    else:
        # todo 如果有多个请求同时执行，这里有可能会有问题（Race Condition），需要用到F()
        selected_choice.votes += 1
        selected_choice.save()
        # 在成功处理POST的数据后返回一个HttpResponseRedirect。
        # 这可以避免当用户按下后退按钮时提交两次post
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """返回最近发布的五条question"""
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """排除还未到发布日期的question"""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
