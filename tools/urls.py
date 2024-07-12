from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage),
    path("signup/", views.signup, name="signup"),
    path("tool-details/", views.submit_rating, name="tool_details"),
]
