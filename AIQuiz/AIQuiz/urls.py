
from django.contrib import admin
from django.urls import path, include
from Quiz import views 
from rest_framework import routers



router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'choices', views.ChoiceViewSet)
router.register(r'question_submissions', views.QuestionSubmissionViewSet)
router.register(r'quiz_submissions', views.QuizSubmissionViewSet)

urlpatterns = [
    path('', include(router.urls)),  # API root
    path('admin/', admin.site.urls), # admin page
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')) # API authentication

]
