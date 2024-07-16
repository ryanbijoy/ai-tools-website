from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage),
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("tool-details/", views.submit_rating, name="tool_details"),
    path("terms-of-services/", views.terms_of_service, name="terms_of_service"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate,
         name='activate'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
]
