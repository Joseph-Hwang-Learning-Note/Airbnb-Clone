import os
from django.contrib.auth.forms import UserCreationForm
import requests

# from django.forms.forms import Form
from django.views.generic import FormView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

# from django.views import View
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.core.files.base import ContentFile

# from django.shortcuts import render
from django.contrib.auth import logout, authenticate, login
from . import forms, models, mixins
from django.contrib import messages


class LoginView(mixins.LoggedOutOnlyView, FormView):  # Order Matters

    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


# class LoginView(View):  # We Also got LoginView (But it uses username, not email)
#     def get(self, request):
#         form = forms.LoginForm()
#         return render(
#             request,
#             "users/login.html",
#             {
#                 "form": form,
#             },
#         )

#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#         return render(
#             request,
#             "users/login.html",
#             {
#                 "form": form,
#             },
#         )


def log_out(request):  # We also got LogoutView
    messages.info(request, "See you later")
    logout(request)
    return redirect(reverse("core:home"))


class SignupView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    # initial = {}

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # to do: add error message
        pass

    return redirect(reverse("core:home"))


def github_login(request):
    cliend_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={cliend_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):

    pass


def github_callback(request):
    print(request.GET)
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        print(client_id, client_secret, code)
        print("1")
        if code is not None:
            print("2")
            result = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            print(result)
            result_json = result.json()
            error = result_json.get("error", None)
            print(error)
            print(result_json)
            if error is not None:
                print("3")
                raise GithubException("Can't get access token")
            else:
                print("4")
                access_token = result_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                print(profile_json)
                username = profile_json.get("login", None)
                print(username)
                if username is not None:
                    print("5")
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    # bio = profile_json.get("bio")
                    print(type(name), type(email))
                    try:
                        print("6")
                        user = models.User.objects.get(email=email)
                        print(user, email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            print("7")
                            raise GithubException(
                                f"Please log in with: {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        print("8")
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            login_method="github",
                            username=email,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        print(user, email)
                        user.save()
                    print("8.5")
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    print("9")
                    raise GithubException("Can't get your profile")
        else:
            print("10")
            raise GithubException("Can't get code")
    except Exception as err:
        print("11")
        messages.error(request, err)
        return redirect(reverse("users:login"))


def kakao_login(request):
    app_key = os.environ.get("K_KEY")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        client_id = os.environ.get("K_KEY")
        code = request.GET.get("code")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}",
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get authorization code")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        email = profile_json.get("kakao_account", None).get("email", None)

        if email is None:
            raise KakaoException("Please also give me your email")
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with: {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                first_name=nickname,
                login_method="kakao",
                email_verified=True,
                username=email,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content())
                )
        login(request, user)
        messages.success(request, f"Welcome back {user.first_name}")
        return redirect(reverse("core:home"))
    except KakaoException as err:
        messages.error(request, err)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    template_name = "users/user_detail.html"
    model = models.User
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Always super() !!
        return context


class UpdateProfileView(mixins.LoggedInOnlyView, UpdateView, SuccessMessageMixin):

    form_class = forms.UpdateProfileForm
    template_name = "users/update_profile.html"
    context_object_name = "user"
    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        self.object.username = email
        self.object.save()
        return super().form_valid(form)


class UpdatePasswordView(
    mixins.LoggedInOnlyView,
    mixins.EmailLoginOnlyView,
    PasswordChangeView,
    SuccessMessageMixin,
):

    template_name = "users/update_password.html"
    success_message = "Password Changed"

    def get_form(self, form_class=forms.UpdatePasswordForm):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Old Password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New Password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "New Password Confirm"
        }
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()
