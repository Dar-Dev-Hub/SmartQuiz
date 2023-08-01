
from django.contrib import admin
from django.urls import path, include
from Quiz import views 
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(
        title="Quiz API",
        default_version='v1',
        description="Quiz API",
        contact=openapi.Contact(email="ahmedbelhaj.it@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(),
)

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'choices', views.ChoiceViewSet)
router.register(r'question_submissions', views.QuestionSubmissionViewSet)
router.register(r'quiz_submissions', views.QuizSubmissionViewSet)

# router.register(r'quiz', views.QuestionSuggestionsView)
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('', include(router.urls)),  # API root
    path('admin/', admin.site.urls), # admin page
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')) # API authentication

]
