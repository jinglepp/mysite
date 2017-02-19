from django.test import TestCase

# Create your tests here.
import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question


class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """pub_date是还没到的时间时，was_published_recently()应该返回False"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """pub_date超出一天内时was_published_recently()返回False"""
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """pub_date在最近一天内时was_published_recently()返回True"""
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """用指定的question_textt和当前日期之前的天数days创建一个question"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionViewTest(TestCase):
    def test_index_view_with_no_question(self):
        """如果没有question存在，应该显示相应的提示"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "目前没有可用Polls。")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """最近一天内提交的question应该显示"""
        create_question(question_text="提交测试question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: 提交测试question>']
        )

    def test_index_view_a_future_question(self):
        """pub_date在未来的不应该显示"""
        create_question(question_text="提交测试question", days=-30)
        create_question(question_text="未到提交日期的question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: 提交测试question>']
        )

    def test_index_view_two_past_question(self):
        """应该显示多个question"""
        create_question(question_text="提交测试question1", days=-30)
        create_question(question_text="提交测试question2", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: 提交测试question2>', '<Question: 提交测试question1>']
        )


class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """访问未到发布日期的question时返回404"""
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """显示questin的详情页应该显示question_text"""
        past_question = create_question(question_text='Past Question', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
