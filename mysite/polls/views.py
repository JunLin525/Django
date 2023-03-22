from django.template import loader
from .models import Question, Choice
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404, render#, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views import generic
from .models import Others
from django.contrib.auth.views import LoginView
#from django.contrib.auth import login
#from .forms import Registration

class CustomLoginView(LoginView): #don't overwrite loginview
    template_name='polls/login.html'
    fields = '__all__'
    redirect_authenticated_user =True

    def get_success_url(self):
        return HttpResponse('http://127.0.0.1:8000/admin/login/?next=/admin/')

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]
    
    
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def helloworld(request):
    return HttpResponse("hello,world. you are at the polls index.")


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def add_choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = Others(request.POST)
        if form.is_valid():
            choice_text = form.cleaned_data['choice_text']
            question.choice_set.create(choice_text=choice_text)
            return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
    else:
        form = Others()
    return render(request, 'polls/add_choice.html', {'form': form, 'question': question})
