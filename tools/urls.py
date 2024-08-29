from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.homepage, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("tool/<str:name>/", views.submit_rating, name="tool_details"),
    path("terms-of-services/", views.terms_of_service, name="terms_of_service"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
    path("blog/", views.blog, name="blog"),
    path("logout/", views.user_logout, name="logout"),
    path("reset-password/", views.CustomPasswordResetView.as_view(template_name="login.html"), name="password_reset"),
    path("reset-password-sent/", auth_views.PasswordResetDoneView.as_view(template_name="login.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name="password-reset.html"), name="password_reset_confirm"),
    path("reset-password-complete/", auth_views.PasswordResetCompleteView.as_view(template_name="reset-password-done.html"), name="password_reset_complete"),
    path('login-modal/', views.authentication_modal_view, name='login_modal'),
    path('contact/', views.contact, name='contact'),
]
