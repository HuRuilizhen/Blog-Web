from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from .forms import *
from django.db.models import F, Window
from django.db.models.functions import Rank


def get_rank(profile):
    ranked_profiles = Profile.objects.annotate(
        rank=Window(expression=Rank(), order_by=F("score").desc())
    )

    rank = ranked_profiles.get(id=profile.id).rank
    return rank


def home_view(request):
    if request.user.is_authenticated:
        current_user = request.user
        profile = current_user.profile
        rank = get_rank(profile)
        context = {"profile": profile, "rank": rank}
        return render(request, "home.html", context)
    else:
        return render(request, "home.html")


def user_home_view(request, user_id):
    owner_user = User.objects.get(id=user_id)
    profile = owner_user.profile
    rank = get_rank(profile)
    context = {"profile": profile, "rank": rank}
    return render(request, "user_home.html", context)


def login_view(request):
    if request.method != "POST":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                url = reverse("contents:personal_blogs")
                return redirect(url)
            else:
                form.add_error(None, "invalid login form")
        return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/home/")


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            Profile.objects.create(user=user, sex_type=request.POST.get("sex_type"))

            url = reverse("users:home")
            return redirect(url)
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})


@login_required
def edit_profile_view(request):
    current_user = request.user
    current_profile = current_user.profile
    personal_homepage_form = ProfilePersonalHomepageForm(instance=current_profile)
    new_password_1 = ""
    new_password_2 = ""
    error_info = ""

    context = {
        "profile": current_profile,
        "personal_homepage_form": personal_homepage_form,
        "new_password_1": new_password_1,
        "new_password_2": new_password_2,
        "error_info": error_info,
    }

    return render(request, "edit_profile.html", context)


@login_required
def edit_profile_user_description_view(request):
    current_user = request.user
    current_profile = current_user.profile
    personal_homepage_form = ProfilePersonalHomepageForm(instance=current_profile)
    new_password_1 = ""
    new_password_2 = ""
    error_info = ""

    if request.method == "POST":
        current_profile.user_description = request.POST.get("user_description")
        current_profile.save()

    context = {
        "profile": current_profile,
        "personal_homepage_form": personal_homepage_form,
        "new_password_1": new_password_1,
        "new_password_2": new_password_2,
        "error_info": error_info,
    }

    return render(request, "edit_profile.html", context)


@login_required
def edit_profile_user_photo_url_view(request):
    current_user = request.user
    current_profile = current_user.profile
    personal_homepage_form = ProfilePersonalHomepageForm(instance=current_profile)
    new_password_1 = ""
    new_password_2 = ""
    error_info = ""

    if request.method == "POST":
        current_profile.user_photo_url = request.POST.get("user_photo_url")
        current_profile.save()

    context = {
        "profile": current_profile,
        "personal_homepage_form": personal_homepage_form,
        "new_password_1": new_password_1,
        "new_password_2": new_password_2,
        "error_info": error_info,
    }

    return render(request, "edit_profile.html", context)


@login_required
def edit_profile_personal_homepage_view(request):
    current_user = request.user
    current_profile = current_user.profile
    personal_homepage_form = ProfilePersonalHomepageForm(instance=current_profile)
    new_password_1 = ""
    new_password_2 = ""
    error_info = ""

    if request.method == "POST":
        personal_homepage_form = ProfilePersonalHomepageForm(
            request.POST, instance=current_profile
        )
        personal_homepage_form.save()

    context = {
        "profile": current_profile,
        "personal_homepage_form": personal_homepage_form,
        "new_password_1": new_password_1,
        "new_password_2": new_password_2,
        "error_info": error_info,
    }

    return render(request, "edit_profile.html", context)


@login_required
def edit_profile_password_view(request):
    current_user = request.user
    current_profile = current_user.profile
    personal_homepage_form = ProfilePersonalHomepageForm(instance=current_profile)

    if request.method == "POST":
        new_password_1 = request.POST.get("new_password_1")
        new_password_2 = request.POST.get("new_password_2")

        if new_password_1 == new_password_2:
            current_user.set_password(new_password_1)
            current_user.save()
            return redirect("/home/")

        error_info = "密码不一致"

    context = {
        "profile": current_profile,
        "personal_homepage_form": personal_homepage_form,
        "new_password_1": new_password_1,
        "new_password_2": new_password_2,
        "error_info": error_info,
    }

    return render(request, "edit_profile.html", context)


def ranklist_view(request):
    profiles = Profile.objects.order_by("-score")
    number_of_users = Profile.objects.count()
    context = {"profiles": profiles, "number_of_users": number_of_users}
    return render(request, "ranklist.html", context=context)
