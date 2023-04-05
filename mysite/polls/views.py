from django.template import loader
from .models import Question, Choice
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views import generic
from .models import Others
from django.contrib.auth.views import LoginView
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Question
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic import DetailView
from .forms import QuestionForm,ChoiceForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView


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
        return Question.objects.order_by('-pub_date')[:20]
    
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:20]


class DetailView(generic.DetailView):   
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def helloworld(request):
    return HttpResponse("hello,world. you are at the polls index.")


def question_list(request):
    questions=Question.objects.filter(user=request.user)
    return render(request, 'polls/detail.html', {'questions':questions})

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


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('polls/login.html')
    else:
        form = AuthenticationForm()
    return render(request, 'polls/login.html', {'form': form})

def logout_user(request):
    pass
class CreateQuestionView(LoginRequiredMixin, CreateView):
    template_name = 'create_question.html'
    form_class = QuestionForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CreateChoiceView(LoginRequiredMixin, CreateView):
    template_name = 'create_choice.html'
    form_class = ChoiceForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super().form_valid(form)


from .forms import QuestionForm, ChoiceForm

def create_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        choice_form = ChoiceForm(request.POST)
        if question_form.is_valid() and choice_form.is_valid():
            question = question_form.save(commit=False)
            question.user = request.user #设置问题的用户为当前登录用户
            question.save()
            choice = choice_form.save(commit=False)
            choice.question = question
            choice.save()
            return redirect('question_detail', pk=question.pk)
    else:
        question_form = QuestionForm()
        choice_form = ChoiceForm()
    return render(request, 'polls/create_question.html', {'question_form': question_form, 'choice_form': choice_form})


#class MyDetailView(DetailView):
#    model = MyModel
#    template_name = 'my_template.html'

#    def dispatch(self, request, *args, **kwargs):
#        if not request.user.is_authenticated:
#            return redirect('login_url')
#        return super().dispatch(request, *args, **kwargs) 