from django.contrib import admin
from .models import Question, Choice, QuizSubmission, QuestionSubmission
# Register your models here.


admin.site.register(Choice, list_display=['content', 'question', 'is_correct'])
admin.site.register(Question, list_display=('content', 'weight', 'level')
                    )
admin.site.register(QuizSubmission, list_display=[
                    'user', 'score', 'start_time', 'end_time', 'status', 'max_questions'])
admin.site.register(QuestionSubmission, list_display=["user", "question", "is_correct", "timestamp"])
