from django.shortcuts import render

def mypage_view(request):
    return render(request, 'mypage/myp.html')

def myp_info(request):
    return render(request, 'mypage/myp_info.html')

def myp_self(request):
    return render(request, 'mypage/myp_self.html')

def myp_survey(request):
    return render(request, 'mypage/myp_survey.html')
