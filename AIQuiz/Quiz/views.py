from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, Choice, UserProfile

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
    return total_score


