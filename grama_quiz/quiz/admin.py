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

# Register your models here.
admin.site.register(Team)
admin.site.register(Answer)
admin.site.register(Option)
admin.site.register(Question, QuestionAdmin)