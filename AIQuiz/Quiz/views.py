from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Question, Choice, QuestionSubmission, QuizSubmission
from rest_framework import viewsets
# from rest_framework import permissions
from Quiz.serializers.user import UserSerializer, GroupSerializer
from Quiz.serializers.quiz import  QuestionSerializer, ChoiceSerializer,QuestionSubmissionSerializer,QuizSubmissionSerializer
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


class QuizSubmissionViewSet(viewsets.ModelViewSet):
    queryset = QuizSubmission.objects.all()
    serializer_class = QuizSubmissionSerializer

    def list(self, request, *args, **kwargs):
        user = request.user  # Assuming you have authentication set up and can get the user
        last_response = user.questionsubmission_set.last()  # Get the last response for the user

        if last_response is None:
            # If there is no previous response, return an empty list of quiz submissions
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        # Get the related question based on the last response
        last_question = last_response.question
        # Get suggestions for the next question based on the last response
        suggestions = Choice.objects.filter(question=last_question).exclude(pk=last_response.choice.pk)

        # Serialize the suggestions for the next question
        suggestion_serializer = ChoiceSerializer(suggestions, many=True)
        
        # Return the suggestions along with the list of quiz submissions
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'quiz_submissions': serializer.data,
            'suggested_choices': suggestion_serializer.data
        })
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class QuestionSubmissionViewSet(viewsets.ModelViewSet):
    queryset = QuestionSubmission.objects.all()
    serializer_class = QuestionSubmissionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]