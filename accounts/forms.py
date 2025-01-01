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

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirmed_password = cleaned_data.get("confirm_password")
        if password != confirmed_password:
            raise forms.ValidationError("Passwords do not match")

        return super().clean()

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
