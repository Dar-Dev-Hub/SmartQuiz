from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Question, Choice, QuestionSubmission, QuizSubmission
from rest_framework import viewsets,generics
from rest_framework import permissions
from Quiz.serializers.user import UserSerializer, GroupSerializer
from Quiz.serializers.quiz import  QuestionSerializer, ChoiceSerializer,QuestionSubmissionSerializer,QuizSubmissionSerializer
from django.contrib.auth.models import User, Group





class QuizSubmissionViewSet(viewsets.ModelViewSet):
    queryset = QuizSubmission.objects.all()
    serializer_class = QuizSubmissionSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class QuestionSubmissionViewSet(viewsets.ModelViewSet):
    queryset = QuestionSubmission.objects.all()
    serializer_class = QuestionSubmissionSerializer




class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
