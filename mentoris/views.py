from django.http import HttpResponse
from django.template import loader
from mentapp.models import User, Email
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail


def katex(request):
    template = loader.get_template("katex/index.html")
    return HttpResponse(template.render())


def sign_up(request):
    template = loader.get_template("mentapp/sign_up.html")
    return HttpResponse(template.render())


def profile(request):
    template = loader.get_template("mentapp/profile.html")
    return HttpResponse(template.render())


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(display_name=username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            # TODO: log user in
            return redirect(f"../profile/{user.user_id}")
        else:
            messages.error(
                request,
                "Could not find account, please double-check account credentials",
            )
            return render(
                request,
                "mentapp/login.html",
                {"username": username, "password": password},
            )
    else:
        return render(
            request,
            "mentapp/login.html",
        )


def user_info(request, user_id):
    user_profile = get_object_or_404(User, user_id=user_id)
    email = get_object_or_404(Email, user_id=user_id)
    return render(
        request, "mentapp/profile.html", {"user_profile": user_profile, "email": email}
    )


def request_translation(request, user_id):
    # need to verify email to ses when they sign up in order for this to work
    email = get_object_or_404(Email, user_id=user_id, is_primary=True)
    primary_language = get_object_or_404(User.primary_language, user_id=user_id)
    send_mail(
        "Kontinua Quiz Questions Translations Request",
        "Hi there! We have noticed you are fluent in "
        + primary_language
        + ". This week these questions were added in "
        + primary_language
        + ". I can do a preliminary translation to "
        + primary_language
        + " using Google Translate. Would you look at and correct those preliminary translations?  Click here.",
        "notifications@kontinua.org",
        [email],
    )
