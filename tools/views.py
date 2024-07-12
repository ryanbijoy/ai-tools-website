from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import AiTool, ToolRating
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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

@login_required
def submit_rating(request):
    email = request.user.email
    ai_tool = request.POST.get('ai_tool')
    star_rating = request.POST.get('star_rating')

    if request.method == "POST":
        ToolRating.objects.create(email=email, ai_tool=ai_tool, rating=star_rating)

    return render(request, 'tool-details.html')
