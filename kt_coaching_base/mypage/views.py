from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password

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
from django.shortcuts import render, redirect
from django.contrib import messages

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
        
        return redirect(f"{reverse('mypage:popup')}?message=프로필 정보가 성공적으로 업데이트 되었습니다.")

    else:
        return render(request, 'mypage/myp_info.html')
    
def popup(request):
    message = request.GET.get('message', None)
    return render(request, 'mypage/myp_popup.html', {'message': message})

# 마이페이지 접속 시 비밀번호 한 번 더 
# def password_check(request):
#     if request.is_ajax() and request.method == 'POST':
#         password = request.POST.get("password", None)
#         if password and check_password(password, request.user.password):
#             return JsonResponse({"result": True})
#         else:
#             return JsonResponse({"result": False})

#     return JsonResponse({"result": False})


