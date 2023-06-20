from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def mypage_view(request):
    return render(request, 'mypage/myp.html')

def box_info(request):
    return render(request, 'mypage_info/myp_info.html')

def box_self(request):
    return render(request, 'mypage_self/myp_self.html')

def box_survey(request):
    return render(request, 'mypage_survey/myp_survey.html')
