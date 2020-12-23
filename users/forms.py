from django import forms
from django.db.models import fields
from django.forms import widgets
from . import models
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data  # Always need to return this!!
            else:
                self.add_error("password", forms.ValidationError("Password is Wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


# class SignUpForm(UserCreationForm):

#     username = forms.EmailField(
#         label="Email"
#     )  # 이거 쓰기 싫으면  password_validation.validate_password(password,self.instance) 써라


# class SignUpForm(UserCreationForm):

#     email = forms.EmailField()

#     class Meta:
#         model = models.User
#         fields = ("email",)


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email Name"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    passwordConfirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    def clean_passwordConfirm(self):
        password = self.cleaned_data.get("password")
        passwordConfirm = self.cleaned_data.get("passwordConfirm")

        if password != passwordConfirm:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()


# class SignUpForm(forms.Form):

#     first_name = forms.CharField(
#         max_length=80,
#         widget=forms.TextInput(attrs={"placeholder": "First Name"}),
#     )
#     last_name = forms.CharField(
#         max_length=80,
#         widget=forms.TextInput(attrs={"placeholder": "Last Name"}),
#     )

#     email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
#     )
#     passwordConfirm = forms.CharField(
#         widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
#     )

#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         try:
#             models.User.objects.get(email=email)
#             raise forms.ValidationError("User already exists with that email")
#         except models.User.DoesNotExist:
#             return email

#     def clean_passwordConfirm(self):
#         password = self.cleaned_data.get("password")
#         passwordConfirm = self.cleaned_data.get("passwordConfirm")

#         if password != passwordConfirm:
#             raise forms.ValidationError("Password confirmation does not match")
#         else:
#             return password

#     def save(self):
#         first_name = self.cleaned_data.get("first_name")
#         last_name = self.cleaned_data.get("last_name")
#         email = self.cleaned_data.get("email")
#         password = self.cleaned_data.get("password")
#         user = models.User.objects.create_user(email, email, password)
#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()
