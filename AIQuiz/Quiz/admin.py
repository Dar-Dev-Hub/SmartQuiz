from django.contrib import admin
from .models import Question, Choice, QuizSubmission, QuestionSubmission
# from rest_framework.authtoken.models import Token

# Register your models here.



@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'level')
    list_filter = ('level',)
    search_fields = ('content',)

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('content', 'question', 'is_correct')
    list_filter = ('question', 'is_correct')
    search_fields = ('content',)

@admin.register(QuizSubmission)
class QuizSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'max_questions',)
    list_filter = ('user',)
    search_fields = ('user__username',)

@admin.register(QuestionSubmission)
class QuestionSubmissionAdmin(admin.ModelAdmin):
    list_display = ('quiz_submission', 'question', 'choice', 'is_correct', 'timestamp')
    list_filter = ('quiz_submission', 'question', 'is_correct')
    search_fields = ('quiz_submission__user__username', 'question__content', 'choice__content',"question__level")