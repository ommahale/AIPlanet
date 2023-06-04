from django.urls import path
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import rest_framework.permissions as permissions

schema_view = get_schema_view(
   openapi.Info(
      title="AI Planet Hackathon Assignment API",
      default_version='v1.0.0',
      description="API for AI Planet Hackathon Assignment",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="omanohar15@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
urlpatterns = [
   path("",views.index),
   path("register/",views.register),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path("hackathon/create",views.CreateHackathonView.as_view()),
   path("hackathon/list",views.ListHackathonView.as_view()),
   path("hackathon/team/register",views.RegisterTeamAPIView.as_view()),
   path("hackathon/team/list",views.get_user_registrations),
   path("hackathon/team/submit",views.CreateSubmissionAPIView.as_view()),
   path("hackathon/team/submissions",views.get_hackathon_submissions),
]