# account/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account
from captcha.fields import CaptchaField

# 회원 가입 폼
class RegistrationForm(UserCreationForm):
    
    class Meta:
        model = Account
        fields = ['userid', 'email', 'username', 'nickname', 'department', 'rank', 'age', 'gender', 'password1', 'password2']

    def clean_id(self):
        userid = self.cleaned_data.get("userid")
        # 필드 길이 제한
        if len(userid) > 32:
            raise forms.ValidationError("ID length should be at most 32 characters.")
        # 이미 존재하는지
        try:
            account = Account.object.get(userid=userid)
        except Exception as e:
            return userid
        raise forms.ValidationError(f"id {userid} is already is use.")

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if len(email) > 45:
            raise forms.ValidationError("Email length should be at most 45 characters.")
        try:
            account = Account.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"email {email} is already is use.")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 45:
            raise forms.ValidationError("Username length should be at most 45 characters.")
        try:
            account = Account.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"username {username} is already is use.")

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if len(nickname) > 45:
            raise forms.ValidationError("Nickname length should be at most 45 characters.")
        try:
            account = Account.objects.get(nickname=nickname)
        except Exception as e:
            return nickname
        raise forms.ValidationError(f"nickname {nickname} is already is use.")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
    
class CaptchaForm(forms.Form):
    captcha = CaptchaField()