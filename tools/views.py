from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from .models import AiTool, ToolRating
from django.contrib.auth.models import User as UserDetail
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .token import account_activation_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


def homepage(request):
    ai_tools = AiTool.objects.all()
    if request.method == "POST":
        prompt = request.POST.get("prompt")

    return render(request, "index.html", {"ai_tools": ai_tools})


def signup(request):
    if request.user and request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = UserDetail.objects.create_user(
                username=form.cleaned_data["email"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }

            html_content = render_to_string('email-verification.html', context)
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                subject=mail_subject, body=text_content, to=[form.cleaned_data.get('email')]
            )
            email.attach_alternative(html_content, "text/html")

            email.send()

            return render(request, "signup.html", {"form": form, "email_confirmation": True})

    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(UserDetail, pk=uid)
    except(TypeError, ValueError, OverflowError, UserDetail.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "verification-success.html")
    else:
        return render(request, "verification-failed.html")


def user_login(request):
    if request.user and request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']

            user = authenticate(request, username=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)
                    return redirect('/')
                else:
                    form.add_error(None, "This account is inactive.")
            else:
                form.add_error(None, "Invalid email or password.")
        else:
            form.add_error(None, "Please correct the errors below.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


@login_required(login_url="/login")
def submit_rating(request):
    ai_tool = request.POST.get('ai_tool')

    if request.method == "POST":
        star_rating = request.POST.get('star_rating')
        ai_tool = request.POST.get('ai_tool')
        update_rating = ToolRating.objects.update_or_create(
            user = request.user,
            ai_tool = ai_tool,
            defaults = {
                "star_rating": star_rating
            }
        )

        total_votes = ToolRating.objects.filter(ai_tool=ai_tool).count()
        return JsonResponse({'success': True, "total_votes": total_votes})

    total_votes = ToolRating.objects.filter(ai_tool=ai_tool).count()
    return render(request, 'tool-details.html', {"total_votes": total_votes})


def blog(request):
    return render(request, "blog.html")

def terms_of_service(request):
    return render(request, "terms-of-service.html")


def privacy_policy(request):
    return render(request, "privacy-policy.html")
