from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import Question, Answer
from results.models import Result, Result_detail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Test
from .forms import TestForm, UploadFileForm
from .functions import handle_uploaded_file

from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

# Create your views here.

class CreateTestView(UserPassesTestMixin,CreateView):

    form_class = TestForm
    model = Test
    success_url = '/test/upload/'

    def test_func(self):
       return self.request.user.is_superuser

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if 'submit' in self.request.POST:
            print('Submit')
        form = TestForm(request.POST)
        if form.is_valid():
            ### Save the test
            form.instance.created_by = self.request.user
            self.object = form.save()
        return redirect('mcqs:test_upload-view', pk=self.object.pk)

class UpdateTestView(UserPassesTestMixin,UpdateView):

    form_class = TestForm
    model = Test

    def test_func(self):
       return self.request.user.is_superuser

class DeleteTestView(UserPassesTestMixin,DeleteView):

    model = Test
    success_url = reverse_lazy('mcqs:main-view')

    def test_func(self):
       return self.request.user.is_superuser

class TestListView(ListView):
    model = Test
    template_name = 'mcqs/main.html'

    # def get_queryset(self):
    #
    #     user_results = Result.objects.filter(user=self.request.user)
    #     print(user_results)
    #     user_tests = Test.objects.exclude(pk__in=user_results)
    #     return user_tests

class ResultListView(UserPassesTestMixin,ListView):
    model = Result
    template_name = 'mcqs/result.html'

    def test_func(self):
       return self.request.user.is_superuser

class UserResultListView(LoginRequiredMixin,ListView):
    model = Result
    template_name = 'mcqs/user_results.html'

    def get_queryset(self):
        return Result.objects.filter(user=self.request.user)

class Result_detailListView(LoginRequiredMixin,ListView):
    model = Result_detail
    template_name = 'mcqs/result_detail.html'

    def get_queryset(self, *args, **kwargs):
        test = self.kwargs['test_name'].split('-')
        test_name = test[0]
        test_topic = test[1]
        test = Test.objects.get(name=test_name, topic=test_topic)
        return Result_detail.objects.filter(user=self.request.user, test_name=test.pk)

class student_Result_detailListView(UserPassesTestMixin,ListView):
    model = Result_detail
    template_name = 'mcqs/result_detail.html'

    def test_func(self):
       return self.request.user.is_superuser

    def get_queryset(self, *args, **kwargs):
        user_name = self.kwargs['user_name']
        user = User.objects.get(username=user_name)
        test = self.kwargs['test_name'].split('-')
        test_name = test[0]
        test_topic = test[1]
        test = Test.objects.get(name=test_name, topic=test_topic)
        return Result_detail.objects.filter(user=user.pk, test_name=test.pk)
#######################################
## Functions that require a pk match ##
#######################################
@login_required
def test_view(request, pk):
    test = Test.objects.get(pk=pk)
    if Result.objects.filter(user=request.user, test_name=test).exists():
            return render(request, 'mcqs/test.html',{'text':'You have already submit the test',
                                                    'test_name':test})
    return render(request, 'mcqs/test.html',{'obj':test})

@login_required
def save_test_view(request, pk):
    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists()) #convert querydictionary into ordinary dictionary

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        test = Test.objects.get(pk=pk)

        score = 0
        multiplier = 100/test.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)
            print("selected",a_selected)
            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
                Result_detail.objects.create(test_name=test, user=user, question=q, selected_answer=a_selected, correct_answer=correct_answer)
            else:
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a.correct:
                        correct_answer = a.text
                results.append({str(q): {'correct_answer': correct_answer, 'answered': 'not answered'}})
                Result_detail.objects.create(test_name=test, user=user, question=q, selected_answer=a_selected, correct_answer=correct_answer)

        score_ = score * multiplier
        Result.objects.create(test_name=test, user=user, score=score_)

        if score_ >= test.passing_score:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})


@login_required
def test_data_view(request, pk):
    test = Test.objects.get(pk=pk)
    questions = []
    for q in test.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': test.time,
    })

@login_required
def upload_file(request, pk):
    test = Test.objects.get(pk=pk)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], test)
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render(request, 'mcqs/upload_test.html', {'form': form})
