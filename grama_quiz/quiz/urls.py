from django.urls import path

from . import views

urlpatterns = [
    path('', views.indexView, name='index'),
    path('questions', views.questionsView, name='questions'),
    path('questions/<int:questionId>', views.answerQuestionView, name='answer'),
    path('waiting', views.waitingView, name='waiting'),
    path('leaderboard', views.leaderboardView, name='leaderboard')
]