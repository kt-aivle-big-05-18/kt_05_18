from django.shortcuts import render, redirect

def mypage_view(request):
    if not request.user.is_authenticated :
        return redirect('account:login')
    else :
        return render(request, 'mypage/myp.html')

def myp_info(request):
    return render(request, 'mypage/myp_info.html')

def myp_self(request):
    return render(request, 'mypage/myp_self.html')

def myp_survey(request):
    return render(request, 'mypage/myp_survey.html')
