# account/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import RegistrationForm, CaptchaForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Account, admin_info
from captcha.fields import CaptchaField
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
#----------------------------------------------------------------------------------------------------------------------#
# 0. 필요 install 목록
# pip install captcha
#----------------------------------------------------------------------------------------------------------------------#

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(request, userid=user.userid, password=form.cleaned_data['password1'])
            login(request, user)
            return redirect("common:home")
    else:
        form = RegistrationForm()
    
    return render(request, 'account/signup.html', {"form": form})

def login_view(request):
    if request.method == 'POST':
        userid = request.POST['userid']
        password = request.POST['password']
        captcha_word = request.POST.get('captcha', '')  # 캡챠 입력값 가져오기
        captcha_key = request.POST.get('captcha_0', '')  # 추가: 캡챠 키 가져오기

        account = Account.objects.filter(userid=userid).first()

        print("cap:", captcha_word)
        print("cap_key:", captcha_key)
        if account and account.password_attempt_count >= 5:
            # 로그인 시도 횟수가 5회 이상인 경우에만 캡챠 표시
            show_captcha = True
            if 'captcha_key' in request.session:
                captcha_key = request.session['captcha_key']
            else:
                captcha_key = CaptchaStore.generate_key()
                request.session['captcha_key'] = captcha_key
            captcha_image_url = '/captcha/image/{}'.format(captcha_key)
            print("if. cap key:", captcha_key)
            print("if. cap:", captcha_word)
            # 캡챠 유효성 검사
            if captcha_key and captcha_word:
                if CaptchaStore.objects.filter(response=captcha_word, hashkey=captcha_key).count() == 0:
                    return render(request, 'account/login.html',
                                  {'error_message': 'Invalid captcha', 'show_captcha': show_captcha,
                                   'captcha_image_url': captcha_image_url, 'captcha_key': captcha_key})
            else:
                return render(request, 'account/login.html',
                              {'error_message': 'Invalid captcha', 'show_captcha': show_captcha,
                               'captcha_image_url': captcha_image_url, 'captcha_key': captcha_key})

            # 비밀번호 검증
            user = authenticate(request, userid=userid, password=password)
            if user is not None:
                login(request, user)
                account.password_attempt_count = 0  # 로그인 성공 시, 로그인 시도 횟수 초기화
                account.save()
                return redirect("common:home")
            else:
                account.password_attempt_count += 1  # 로그인 실패 시, 로그인 시도 횟수 증가
                account.save()
                return render(request, 'account/login.html',
                              {'error_message': 'Invalid login credentials', 'show_captcha': show_captcha,
                               'captcha_image_url': captcha_image_url, 'captcha_key': captcha_key})

        else:
            # 로그인 시도 횟수가 5회 미만인 경우에는 캡챠 표시하지 않음
            show_captcha = False
            captcha_image_url = ''
            captcha_key = ''

            # 비밀번호 검증
            user = authenticate(request, userid=userid, password=password)
            if user is not None:
                login(request, user)
                if account:
                    account.password_attempt_count = 0  # 로그인 성공 시, 로그인 시도 횟수 초기화
                    account.save()
                    admin_info_count = admin_info(
                        count   = 1
                    )
                    admin_info_count.save()
                return redirect("common:home")
            
            else:
                # 로그인 실패 시, 로그인 시도 횟수 증가
                if account:
                    account.password_attempt_count += 1
                    account.save()

                return render(request, 'account/login.html',
                              {'error_message': 'Invalid login credentials', 'show_captcha': show_captcha,
                               'captcha_image_url': captcha_image_url, 'captcha_key': captcha_key})
    else:
        # 로그인 시도 횟수가 5회 이상인 경우에만 캡챠 표시
        password_attempt_count = request.session.get('password_attempt_count', 0)
        show_captcha = password_attempt_count >= 5

        if 'captcha_key' in request.session:
            captcha_key = request.session['captcha_key']
        else:
            captcha_key = CaptchaStore.generate_key()
            request.session['captcha_key'] = captcha_key
        captcha_image_url = '/captcha/image/{}'.format(captcha_key)

        return render(request, 'account/login.html',
                      {'show_captcha': show_captcha, 'captcha_image_url': captcha_image_url, 'captcha_key': captcha_key})

def logout_view(requset):
    logout(requset)
    return redirect("common:home")

@require_POST
def check_duplicate(request):
    userid = request.POST.get('userid', None)

    response_data = {
        'is_taken': Account.objects.filter(userid=userid).exists()
    }

    return JsonResponse(response_data)

