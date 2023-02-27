from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Sum, F
from django.shortcuts import redirect

from .forms import TeamForm
from .models import Question, Team, Option, Answer
from .decorators import with_team_created, without_team_created

from datetime import datetime


@without_team_created
def indexView(request):

    if request.method == 'POST':
        
        form = TeamForm(request.POST)

        if form.is_valid():
            createdTeam = Team(name=form.cleaned_data['name'])
            createdTeam.save()
            print(f'Created team: {createdTeam}')

            request.session['teamId'] = createdTeam.id

            return redirect('questions')
        else:
            return render(request, 'quiz/index.html', {'form': form})
    
    else:
        form = TeamForm()
        return render(request, 'quiz/index.html', {'form': form})


@with_team_created
def questionsView(request):
    
    team = getCurrentTeam(request)
    
    if request.method == 'POST':
        team = getCurrentTeam(request)
        team.hasFinished = True
        team.save()
        return redirect('waiting')

    questions = Question.objects.all().order_by('questionNumber', 'category')
    questions_grouped = {}
    for question in questions:
        if question.category not in questions_grouped:
            questions_grouped[question.category] = []
        questions_grouped[question.category].append(question)

    return render(request, 'quiz/questions.html', {'questions_grouped': questions_grouped, 'team': team})


@with_team_created
def answerQuestionView(request, questionId):
    
    team = getCurrentTeam(request)
    
    question = get_object_or_404(Question, questionNumber=questionId)

    options = Option.objects.filter(question=question)
    isMultiple = options.exists()

    

    try:
        previousAnswer = Answer.objects.get(question=question, team=team)
    except Answer.DoesNotExist:
        previousAnswer = None

    if request.method == 'POST':

        answerText = request.POST.get('choice' if isMultiple else 'text')

        if previousAnswer:
            previousAnswer.text = answerText
            previousAnswer.save()
        else:
            newAnswer = Answer(
                team=team,
                question=question,
                text=answerText
            )
            newAnswer.save()

        return redirect('questions')

    return render(request, 'quiz/answer.html', {
        'question': question,
        'isMultiple': isMultiple,
        'options': options,
        'previousAnswer': previousAnswer,
        'team': team
    })

@with_team_created
def waitingView(request):
    
    team = getCurrentTeam(request)

    if not team.hasFinished:
        return redirect('questions')

    if team.totalPoints == -1:
        answers = Answer.objects.filter(team=team)
        questions = Question.objects.filter(answer__in=answers, answer__text__iexact=F('correctAnswer'))

        team.totalPoints = questions.aggregate(Sum('points'))['points__sum']
        if team.totalPoints == None:
            # Team either pressed finish quiz right away or didn't answer anything
            team.totalPoints = 0
        team.submittedAt = datetime.now()
        team.save()
    
    allTeamsFinished = not Team.objects.exclude(hasFinished=True).exists()

    if allTeamsFinished:
        return redirect('leaderboard')
    else:
        return render(request, 'quiz/waiting.html', {'points': team.totalPoints})
    
@with_team_created
def leaderboardView(request):

    team = getCurrentTeam(request)

    if not team.hasFinished:
        return redirect('questions')
    
    teams = Team.objects.filter(hasFinished=True).order_by('-totalPoints', 'submittedAt')
    
    return render(request, 'quiz/leaderboard.html', {'teams': teams})
    
def error404View(request, exception):
    
    return render(request, 'quiz/error_404.html', status=404)

# HELPER FUNCTIONS

def getCurrentTeam(request) -> Team:
    return Team.objects.get(pk=request.session['teamId'])