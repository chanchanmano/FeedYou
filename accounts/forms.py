from django import forms
from django.contrib.auth.hashers import make_password

from accounts.models import User


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "password",
            "confirm_password",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        # Hash the password
        user.password = make_password(self.cleaned_data["password"])

        # Set the role
        user.role = User.CUSTOMER

        if commit:
            if not user.pk:
                user.save(force_insert=True)
            else:
                user.save(force_update=True)

            self.save_m2m()

        return user
