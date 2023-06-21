# community/forms.py
from django import forms
from .models import Notice

class NoticeForm(forms.ModelForm):
    file = forms.FileField(required=False)  # 파일 필드 추가

    class Meta:
        model = Notice
        fields = ('title', 'content', 'file')  # 파일 필드 추가