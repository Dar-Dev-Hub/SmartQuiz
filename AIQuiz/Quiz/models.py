from django.db import models
from django.contrib.auth.models import User

# Create your models here.

import random

# Custom manager for Question model

class QuestionManager(models.Manager):
    def random_question_for_level(self, level):
        # Get a random question for a given level
        questions = self.filter(level=level)
        if questions.exists():
            return random.choice(questions)
        return None

# Create your models here.


class Question(models.Model):
    content = models.TextField()
    weight = models.PositiveIntegerField(default=1)
    level = models.PositiveIntegerField(default=1)
    # objects = QuestionManager()  # Use the custom manager

    def __str__(self):
        # Display the first 50 characters of the question content
        return self.content[:50]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class QuestionSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Foreign key to Question model
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    # Foreign key to QuizSubmission model
    quiz_submission = models.ForeignKey(
        'QuizSubmission', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.question.content} - Correct: {self.is_correct}"

    def validate(self, choice_id):
        # Check if the choice is correct
        choice = Choice.objects.get(id=choice_id)
        self.choice = choice
        self.is_correct = choice.is_correct
        self.save()
        return self.is_correct


class QuizSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    questions = models.ManyToManyField('Question', through=QuestionSubmission)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    max_questions = models.PositiveIntegerField(default=20)
    status = models.CharField(max_length=20, default='in_progress')

    def __str__(self):
        return f"{self.user.username} - {self.score}"

