from django.shortcuts import render, redirect
from .forms import SignUpForm

# Create your views here.


def homepage(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt")

    return render(request, "index.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("")
    else:
        form = SignUpForm()

    return render("signup.html", {"form": form})
