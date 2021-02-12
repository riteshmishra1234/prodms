from django import forms
from .models import User
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from PIL import Image


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'groups',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    contact = forms.CharField(max_length=10, required=True, help_text='Enter Contact Detail', widget=forms.TextInput
    (attrs={'class': 'form-control', 'id': 'id_contact', 'placeholder': 'Contact'}))
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput
    (attrs={'class': 'form-control', 'id': 'id_avatar', 'placeholder': 'Profile Pic'}))

    class Meta:
        model = User
        fields = ('contact', 'avatar',)
