from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class AddStudentForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {"password": forms.PasswordInput()}

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.role:
            user.role = "student"
        if commit:
            user.set_password(self.cleaned_data["password"])
            user.save()
        return user