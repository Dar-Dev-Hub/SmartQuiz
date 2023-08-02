from rest_framework import serializers
from Quiz.models import QuizSubmission, QuestionSubmission, Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'content', 'level', 'choices']

class QuestionSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSubmission
        fields = ['question', 'choice', 'is_correct', 'timestamp']

class QuizSubmissionSerializer(serializers.ModelSerializer):
    questionsubmission_set = QuestionSubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = QuizSubmission
        fields = ['id', 'user', 'score', 'max_questions', 'questionsubmission_set']