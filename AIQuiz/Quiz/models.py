from django.db import models
from django.contrib.auth.models import User

# Create your models here.

import random



# Create your models here.


class Question(models.Model):
    content = models.TextField()
    weight = models.PositiveIntegerField(default=1)
    level = models.PositiveIntegerField(default=1)

    def __str__(self):
        # Display the first 50 characters of the question content
        return self.content[:50]


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class QuizSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    max_questions = models.PositiveIntegerField(default=20)

    def __str__(self):
        return f"{self.user.username} - {self.score}"




class QuestionSubmission(models.Model):
    quiz_submission = models.ForeignKey(QuizSubmission, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.question} - {self.choice} - {self.is_correct}"