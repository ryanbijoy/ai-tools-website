from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage),
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("tool-details/", views.submit_rating, name="tool_details"),
    path("terms-of-services/", views.terms_of_service, name="terms_of_service"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
]
