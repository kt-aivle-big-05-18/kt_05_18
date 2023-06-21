from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
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

# @login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        
        if 'update-department' in request.POST:
            department = request.POST['department']
            user.department = department            
        elif 'update-rank' in request.POST:
            rank = request.POST['rank']
            user.rank = rank
        elif 'update-password' in request.POST:
            password = request.POST['password']
            if len(password) > 0:
                user.set_password(password)
        
        user.save()
        messages.success(request, '프로필 정보가 성공적으로 업데이트되었습니다.')
        return redirect('mypage:myp_info')
    
    else:
        return render(request, 'mypage/myp_info.html')

