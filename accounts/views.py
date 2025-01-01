from django import forms
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import UserForm


class RegisterUserView(FormView):
    template_name = "accounts/registerUser.html"
    form_class = UserForm
    success_url = reverse_lazy("registerUser")

    def form_valid(self, form: forms.ModelForm):
        form.save()
        messages.success(
            self.request, "Your account has been registered successfully!"
        )
        return super().form_valid(form)
