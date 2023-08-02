
from .models import Question, Choice, QuestionSubmission, QuizSubmission
from rest_framework import viewsets, generics
from Quiz.serializers.user import UserSerializer, GroupSerializer
from Quiz.serializers.quiz import  QuestionSerializer, ChoiceSerializer,QuestionSubmissionSerializer,QuizSubmissionSerializer
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import random
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status



class QuizSubmissionViewSet(viewsets.ModelViewSet):
    queryset = QuizSubmission.objects.all()
    serializer_class = QuizSubmissionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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


# Note : not Implemented
class RandomQuestionView(generics.RetrieveAPIView):
    serializer_class = QuestionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = Question.objects.filter(level=1)
        return random.choice(queryset)







# Note : not Implemented
class UserQuestionSubmissionView(generics.CreateAPIView):
    serializer_class = QuestionSubmissionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        quiz_submission_id = self.kwargs['quiz_submission_pk']
        quiz_submission = QuizSubmission.objects.get(id=quiz_submission_id)

        # Check if the quiz submission has reached the maximum number of questions
        if quiz_submission.questionsubmission_set.count() >= quiz_submission.max_questions:
            return Response({'detail': 'Quiz submission has reached the maximum number of questions.'})

        # Save the question submission and update the quiz submission score
        serializer.save(quiz_submission=quiz_submission, user=user)
        quiz_submission.score += serializer.validated_data['is_correct']
        quiz_submission.save()

        # Get the next random question
        next_question = random.choice(Question.objects.filter(level=quiz_submission.quiz.level))
        next_question_serializer = QuestionSerializer(next_question)

        # Prepare the response
        data = {
            'message': 'Question submission successful.',
            'next_question': next_question_serializer.data
        }
        return Response(data)


# Note : not Implemented
class QuizAdvanceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_next_question(self, user, current_question):
        # Retrieve the QuizSubmission for the user
        quiz_submission = QuizSubmission.objects.filter(user=user).last()

        # Determine the next level of the question based on whether the last question was correct or not
        if current_question.is_correct:
            next_level = current_question.level + 1
        else:
            next_level = current_question.level - 1 if current_question.level > 1 else 1

        # Get the next random question from the determined level
        next_question = Question.objects.filter(level=next_level, is_active=True).order_by('?').first()

        # If no question is found at the determined level, get a random question from any level
        if not next_question:
            next_question = Question.objects.filter(is_active=True).order_by('?').first()

        return next_question

    def get(self, request):
        user = request.user

        # Retrieve the last submitted question by the user
        last_question_submission = QuestionSubmission.objects.filter(
            user=user).order_by('-timestamp').first()

        if last_question_submission:
            current_question = last_question_submission.question
        else:
            # If no previous question submission, get a random question to start the quiz
            current_question = Question.objects.filter(is_active=True).order_by('?').first()

        # Get the next question based on the last question's correctness and user's level
        next_question = self.get_next_question(user, current_question)

        # Serialize the next question and return the response
        next_question_serializer = QuestionSerializer(next_question)
        return Response(next_question_serializer.data, status=status.HTTP_200_OK)