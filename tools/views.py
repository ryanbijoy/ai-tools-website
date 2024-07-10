from django.shortcuts import render, redirect
from .forms import SignUpForm, ToolRatingForm
from django.contrib import messages
from .models import AiTool
from django.contrib.auth.decorators import login_required
# Create your views here.


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
            return redirect("home")  # Replace with your desired redirect URL name
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})


@login_required
def submit_rating(request):
    if request.method == 'POST':
        form = ToolRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.save()
            messages.success(request, 'Thank you for your rating!')
            return redirect('/')
    else:
        form = ToolRatingForm()
    return render(request, 'tool-details.html', {'form': form})
