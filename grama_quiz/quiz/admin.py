from django.contrib import admin

from .models import Team, Question, Answer, Option

class OptionsInLine(admin.StackedInline):
    model = Option
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = [
        OptionsInLine
    ]

def update_team_points(modeladmin, request, queryset):
    for answer in queryset:
        # Get the related team and question objects
        team = answer.team
        question = answer.question

        # Calculate the new total points for the team
        if answer.text == question.correctAnswer:
            team.totalPoints += question.points
        else:
            team.totalPoints -= question.points

        # Save the updated team object
        team.save()

    # Display a success message
    message = f"{len(queryset)} answers updated."
    modeladmin.message_user(request, message)
update_team_points.short_description = "Update team points"

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'question', 'text')
    actions = [update_team_points]

        

# Register your models here.
admin.site.register(Team)
#admin.site.register(Answer)
admin.site.register(Option)
admin.site.register(Question, QuestionAdmin)
