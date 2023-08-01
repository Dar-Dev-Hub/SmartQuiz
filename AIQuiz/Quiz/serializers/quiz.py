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
        fields = '__all__'

class QuestionSubmissionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = QuestionSubmission
        fields = '__all__'

class QuizSubmissionSerializer(serializers.ModelSerializer):
    questionsubmission_set = QuestionSubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = QuizSubmission
        fields = '__all__'
