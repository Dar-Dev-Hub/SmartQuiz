from rest_framework import serializers
from Quiz.models import Quiz, Question, Choice,Category,UserProfile

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title','description']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'content', 'score', 'category', 'score']

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'question', 'content', 'is_correct']

class CategorySerializer(serializers.ModelSerializer):
    class   Meta:
        model = Category
        fields = ['id', 'name', 'description']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'score']