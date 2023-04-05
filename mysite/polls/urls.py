from django.urls import path

from . import views
from .views import user_login
from django.contrib.auth.views import LoginView
from .views import create_question


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('create_question/', views.create_question, name='create_question'),

    #path('<int:pk>/add',views.)
]