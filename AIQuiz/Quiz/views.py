
from rest_framework.decorators import action
from .models import Question, Choice, QuestionSubmission, QuizSubmission
from rest_framework import viewsets, generics
from Quiz.serializers.user import UserSerializer, GroupSerializer
from Quiz.serializers.quiz import QuestionSerializer, ChoiceSerializer, QuestionSubmissionSerializer, QuizSubmissionSerializer
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import random
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action


from django.db import transaction


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def init_quiz(request):
    try:
        with transaction.atomic():
            quiz_submission = QuizSubmission.objects.create(
                user=request.user, score=0)
            question = Question.objects.filter(level=1).first()
            print("Random question = ", question.level , question.id, question.content, question.choices.all())
            if question:
                serializer = QuestionSerializer(question)
                data = {
                    'quiz_submission_id': quiz_submission.id,
                    'question': serializer.data,
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'No questions found.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'detail': 'An error occurred while initializing the quiz.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuizSubmissionViewSet(viewsets.ModelViewSet):
    queryset = QuizSubmission.objects.all()
    serializer_class = QuizSubmissionSerializer
    # permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        quiz_submission = self.get_object()
        serializer = QuestionSubmissionSerializer(data=request.data)
        choice = Choice.objects.get(id=request.data['choice'])
        if serializer.is_valid():
            # Check if the question submission already exists in the quiz submission
            question = serializer.validated_data['question']
            if quiz_submission.questionsubmission_set.filter(question=question).exists():
                if quiz_submission.questionsubmission_set.count() >=  quiz_submission.max_questions:
                    return Response({'detail': 'Quiz completed.', 'score': quiz_submission.score}, status=status.HTTP_200_OK)
                
            else:
                serializer.save(quiz_submission=quiz_submission)
                quiz_submission.score += 1 if choice.is_correct else 0
                quiz_submission.save()
            current_question = Question.objects.get(id=question.id)
            next_question_level = current_question.level + 1 if choice.is_correct == True else current_question.level - 1
            
            
            if int(next_question_level) > 9:
                    next_question_level = 9
            if int(next_question_level) < 1:
                    next_question_level = 1
            # Get the next question that has not been submitted by the user
            next_question = None
            while not next_question:
                next_question = Question.objects.filter(level=next_question_level).exclude(
                    id__in=quiz_submission.questionsubmission_set.values_list(
                        'question', flat=True)
                ).order_by('?').first()

                if not next_question:
                    # If no new question found, end the quiz
                    return Response({'detail': 'Quiz completed.', 'score': quiz_submission.score}, status=status.HTTP_200_OK)

            next_question_serializer = QuestionSerializer(next_question)
            return Response({'next_question': next_question_serializer.data, 'score': quiz_submission.score}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class QuizSubmissionViewSet(viewsets.ModelViewSet):
#     queryset = QuizSubmission.objects.all()
#     serializer_class = QuizSubmissionSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

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

# class QuestionSubmissionViewSet(viewsets.ModelViewSet):
#     queryset = QuestionSubmission.objects.all()
#     serializer_class = QuestionSubmissionSerializer

#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]


# # Note : not Implemented
# class RandomQuestionView(generics.RetrieveAPIView):
#     serializer_class = QuestionSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         queryset = Question.objects.filter(level=1)
#         return random.choice(queryset)


# # Note : not Implemented
# class UserQuestionSubmissionView(generics.CreateAPIView):
#     serializer_class = QuestionSubmissionSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = self.request.user
#         quiz_submission_id = self.kwargs['quiz_submission_pk']
#         quiz_submission = QuizSubmission.objects.get(id=quiz_submission_id)

#         # Check if the quiz submission has reached the maximum number of questions
#         if quiz_submission.questionsubmission_set.count() >= quiz_submission.max_questions:
#             return Response({'detail': 'Quiz submission has reached the maximum number of questions.'})

#         # Save the question submission and update the quiz submission score
#         serializer.save(quiz_submission=quiz_submission, user=user)
#         quiz_submission.score += serializer.validated_data['is_correct']
#         quiz_submission.save()

#         # Get the next random question
#         next_question = random.choice(Question.objects.filter(level=quiz_submission.quiz.level))
#         next_question_serializer = QuestionSerializer(next_question)

#         # Prepare the response
#         data = {
#             'message': 'Question submission successful.',
#             'next_question': next_question_serializer.data
#         }
#         return Response(data)


# # Note : not Implemented
# class QuizAdvanceView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_next_question(self, user, current_question):
#         # Retrieve the QuizSubmission for the user
#         quiz_submission = QuizSubmission.objects.filter(user=user).last()

#         # Determine the next level of the question based on whether the last question was correct or not
#         if current_question.is_correct:
#             next_level = current_question.level + 1
#         else:
#             next_level = current_question.level - 1 if current_question.level > 1 else 1

#         # Get the next random question from the determined level
#         next_question = Question.objects.filter(level=next_level, is_active=True).order_by('?').first()

#         # If no question is found at the determined level, get a random question from any level
#         if not next_question:
#             next_question = Question.objects.filter(is_active=True).order_by('?').first()

#         return next_question

#     def get(self, request):
#         user = request.user

#         # Retrieve the last submitted question by the user
#         last_question_submission = QuestionSubmission.objects.filter(
#             user=user).order_by('-timestamp').first()

#         if last_question_submission:
#             current_question = last_question_submission.question
#         else:
#             # If no previous question submission, get a random question to start the quiz
#             current_question = Question.objects.filter(is_active=True).order_by('?').first()

#         # Get the next question based on the last question's correctness and user's level
#         next_question = self.get_next_question(user, current_question)

#         # Serialize the next question and return the response
#         next_question_serializer = QuestionSerializer(next_question)
#         return Response(next_question_serializer.data, status=status.HTTP_200_OK)
