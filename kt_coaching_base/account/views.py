# account/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm

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
        user = authenticate(request, userid=userid, password=password)
        if user is not None:
            login(request, user)
            return redirect("common:home")  # 로그인 성공 후 리다이렉션할 URL
        else:
            return render(request, 'account/login.html', {'error_message': 'Invalid login credentials'})
    else:
        return render(request, 'account/login.html')
    
def logout_view(requset):
    logout(requset)
    return redirect("common:home")