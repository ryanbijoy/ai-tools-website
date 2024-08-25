from django.shortcuts import render, redirect
from django.contrib.auth.models import User as UserDetail
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import logout, login, authenticate, views as auth_views
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .token import account_activation_token
from .forms import SignUpForm, LoginForm, ContactForm
from .models import AiTool, ToolRating, Category
from .promotion import multi_promotion, testimonials, promotion_card
from .llm_model.input import ask_question
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse


def homepage(request):
    ai_tools = None
    categories = Category.objects.prefetch_related('toolcategory').filter(active=True)

    if request.method == 'POST':
        user_prompt = request.POST.get("prompt")
        if user_prompt:
            result = json.loads(ask_question(user_prompt))
            ai_tools = AiTool.objects.filter(ai_tool__in=result)
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                tools_data = []
                for tool in ai_tools:
                    tools_data.append({
                        'name': tool.ai_tool,
                        'category': tool.category.first().title if tool.category.exists() else '',
                        'description': tool.description,
                        'logo': tool.logo,
                        'website_url': tool.website_url,
                        'avg_rating': tool.avg_rating(),
                        'total_votes': tool.total_votes(),
                    })
                return JsonResponse({'tools': tools_data})

    return render(request, "index.html", {"ai_tools": ai_tools, "categories": categories, "category_count": categories.count(),
                "multi_promotion": multi_promotion, "testimonial": testimonials, "card": promotion_card})


def signup(request):
    if request.user.is_authenticated:
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

            html_content = render_to_string('verification-email.html', context)
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


def user_logout(request):
    logout(request)
    return redirect("/")


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


def authentication_modal_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(email, password)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = LoginForm()
    
    return render(request, 'authentication-modal.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
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


def submit_rating(request, name):
    url_tool_name = name.lower()
    if name != url_tool_name:
        return redirect('tool_details', name=url_tool_name)
    ai_tool = get_object_or_404(AiTool, ai_tool__iexact=url_tool_name)

    if request.method == "POST":
        star_rating = request.POST.get('star_rating')
        review = request.POST.get('review').strip()

        if star_rating:
            ToolRating.objects.update_or_create(
                user=request.user,
                ai_tool=ai_tool,
                defaults={"star_rating": star_rating}
            )

        if review:
            ToolRating.objects.update_or_create(
                user=request.user,
                ai_tool=ai_tool,
                defaults={"review": review if review else None}
            )

        return JsonResponse({'success': True})

    return render(request, 'tool-details.html', {"ai_tool": ai_tool})


class CustomPasswordResetView(auth_views.PasswordResetView):
    email_template_name = 'reset-password-email.html'
    html_email_template_name = 'reset-password-email.html'
    success_url = reverse_lazy('password_reset_done')


def blog(request):
    return render(request, "blog.html")


def tool_categories(request):
    ai_tool = AiTool.objects.all()

    return render(request, "category.html", {"ai_tools": ai_tool})


def terms_of_service(request):
    return render(request, "terms-of-service.html")


def privacy_policy(request):
    return render(request, "privacy-policy.html")


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Compose email
            full_message = f"Name: {first_name} {last_name}\nEmail: {email}\n\nMessage:\n{message}"
            
            try:
                send_mail(
                    subject,
                    full_message,
                    email,  # From email
                    ['ryanbijoy2007@gmail.com'],  # To email
                    fail_silently=False,
                )
                return JsonResponse({'status': 'OK'})
            except Exception as e:
                return JsonResponse({'status': 'ERROR', 'message': str(e)})
        else:
            return JsonResponse({'status': 'ERROR', 'message': form.errors})

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
