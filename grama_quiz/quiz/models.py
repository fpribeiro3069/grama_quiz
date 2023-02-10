from django.db import models

from datetime import datetime

# Create your models here.
class Question(models.Model):
    questionNumber = models.IntegerField(unique=True)
    shortName = models.CharField(max_length=100, default='shortName')
    category = models.CharField(max_length=50)
    correctAnswer = models.CharField(null=False, max_length=500)
    points = models.IntegerField()

    def __str__(self):
        return f'Question {self.questionNumber} worth {self.points} points'
    
class Option(models.Model):
    value = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.value

class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)
    answers = models.ManyToManyField(
        Question,
        through='Answer',
        through_fields=('team', 'question')
    )
    hasFinished = models.BooleanField(default=False)
    totalPoints = models.IntegerField(default=-1)
    submittedAt = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f'Team {self.name}'
    
class Answer(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(null=True, max_length=500)

    class Meta:
        unique_together = (("team", "question"))

    def __str__(self):
        return f'Answer to Q{self.question.questionNumber} of {self.team}'
    