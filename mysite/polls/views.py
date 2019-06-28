from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice
from .mixins import RequireLoginMixin


class VoteView(generic.View):

    def get_queryset(self, choice_id):
        return Choice.objects.get(pk=choice_id)

    def post(self, request, question_id):
        choice_id = request.POST.get('choice', None)
        try:
            query_set = self.get_queryset(choice_id)
        except (KeyError, Choice.DoesNotExist):
            return redirect


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

"""
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = { 'latest_question_list' : latest_question_list }
    return HttpResponse(template.render(context,request))
"""

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        )

"""
def detail(request,question_id):
    try :
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist :
        raise Http404("Question not exit.")

    return (render(request,'polls/detail.html',{ 'question' : question }))
"""

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

"""
def results(request,question_id):
    question =  get_object_or_404(Question,pk=question_id)
    return render(request,'polls/results.html',{'question' : question})
"""

class DeleteView(generic.DetailView):
    model = Question
    success_url = '/polls/'


def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return (render(request, 'polls/detail.html',{
            'question' : question,
            'error_message': "You didn't select a choice.",
        }))
    else:
        selected_choice.votes += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

