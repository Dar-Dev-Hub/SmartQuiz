from django.contrib import admin
from .models import Question, Choice, UserProfile, Quiz, Category
# Register your models here.


admin.site.register(Question,
                    list_display=['content', 'quiz', 'category', 'score'],)
admin.site.register(Choice,list_display=['content', 'question', 'is_correct'])
admin.site.register(Quiz, list_display=['title', 'description'])
admin.site.register(UserProfile, list_display=['user', 'score'])
admin.site.register(Category, list_display=['name', 'description']  )