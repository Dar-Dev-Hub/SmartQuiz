from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, Choice, UserProfile, Category
from rest_framework import viewsets
from rest_framework import permissions
from Quiz.serializers.user import UserSerializer, GroupSerializer
from Quiz.serializers.quiz import QuizSerializer, QuestionSerializer, ChoiceSerializer,CategorySerializer,UserProfileSerializer
from django.contrib.auth.models import User, Group

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.question_set.all()
    context = {'quiz': quiz, 'questions': questions}
    return render(request, 'quiz_detail.html', context)

def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        questions = quiz.question_set.all()
        score = 0

        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                selected_choice = question.choice_set.get(pk=selected_choice_id)
                if selected_choice.is_correct:
                    score += question.score

        # Save the user's score to the profile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.score = score
        user_profile.save()

        return redirect('quiz_results', quiz_id=quiz_id)

def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    user_profile = get_user_profile(request.user)
    user_score = user_profile.score if user_profile else 0
    total_score = calculate_total_score(quiz)
    context = {'quiz': quiz, 'user_score': user_score, 'total_score': total_score}
    return render(request, 'quiz_results.html', context)

def get_user_profile(user):
    try:
        user_profile = UserProfile.objects.get(user=user)
        return user_profile
    except UserProfile.DoesNotExist:
        return None

def calculate_total_score(quiz):
    questions = quiz.question_set.all()
    total_score = sum(question.score for question in questions)

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    get UserProfile By ID
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
class QuizViewSet(viewsets.ModelViewSet):
    """
    get Quiz By ID
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    """
    get Question By ID
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceViewSet(viewsets.ModelViewSet):
    """
    get Choice By ID
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    get Category By ID
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

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
