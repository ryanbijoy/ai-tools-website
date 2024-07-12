from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from .models import AiTool, ToolRating
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def homepage(request):
    ai_tools = AiTool.objects.all()
    if request.method == "POST":
        prompt = request.POST.get("prompt")

    return render(request, "index.html", {"ai_tools": ai_tools})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires on browser close
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


@login_required
def submit_rating(request):
    email = request.user.email
    ai_tool = request.POST.get('ai_tool')
    star_rating = request.POST.get('star_rating')

    if request.method == "POST":
        ToolRating.objects.create(email=email, ai_tool=ai_tool, rating=star_rating)

    return render(request, 'tool-details.html')


def terms_of_service(request):
    return render(request, "terms-of-service.html")


def privacy_policy(request):
    return render(request, "privacy-policy.html")
