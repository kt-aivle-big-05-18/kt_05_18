from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Sum
from rpg.models import Persona, Message
from account.models import Account
from community.models import Survey, Rating
from django.urls import reverse
from django.contrib.auth.hashers import check_password

@login_required
def mypage_view(request):
    if not request.user.is_authenticated :
        return redirect('account:login')
    else :
        return render(request, 'mypage/myp.html')

@login_required
def myp_info(request):
    return render(request, 'mypage/myp_info.html')

@login_required
def myp_survey(request):
    user = request.user.nickname
    personas = Persona.objects.filter(nickname=user)
    messages = Message.objects.filter(persona__in=personas)
    
    context = {
        'personas': personas,
        'messages': messages
    }
    
    return render(request, 'mypage/myp_survey.html', context)

@login_required
@require_POST
def share_persona(request, persona_id):
    try:
        persona = Persona.objects.get(pk=persona_id, nickname=request.user.nickname)
        persona.shared = True
        persona.save()

        title = request.POST.get('title')
        content = request.POST.get('content')

        author = Account.objects.get(nickname=request.user.nickname)
        survey = Survey(author=author, persona_id=persona, title=title, content=content)
        survey.save()

    except Persona.DoesNotExist:
        return redirect('mypage:myp_survey')

    return redirect('mypage:myp_survey')

@login_required
def stop_sharing(request, persona_id):
    try:
        persona = Persona.objects.get(pk=persona_id, nickname=request.user.nickname)
        persona.shared = False
        persona.save()
        
        author = Account.objects.get(nickname=request.user.nickname)
        surveys = Survey.objects.filter(author=author, persona_id=persona, shared=True)
        surveys.update(shared=False)

    except Persona.DoesNotExist:
        return redirect('mypage:myp_survey')

    return redirect('mypage:myp_survey')

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
    
def rating_list(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)
    ratings = Rating.objects.filter(survey__persona_id=persona)

    group_counts = {
        'G': [0, 0, 0, 0],
        'R': [0, 0, 0, 0],
        'O': [0, 0, 0, 0],
        'W': [0, 0, 0, 0],
    }

    for rating in ratings:
        for i in range(1, 15):
            score = getattr(rating, f'score_{i}')
            if 1 <= i <= 3:
                group = 'G'
            elif 4 <= i <= 7:
                group = 'R'
            elif 8 <= i <= 10:
                group = 'O'
            elif 11 <= i <= 14:
                group = 'W'
            else:
                group = None

            if group:
                group_counts[group][score-1] += 1

    context = {
        'persona': persona,
        'ratings': ratings,
        'group_counts': group_counts,
    }
    print("gc:", group_counts)
    return render(request, 'mypage/rating_list.html', context)

def popup(request):
    message = request.GET.get('message', None)
    return render(request, 'mypage/myp_popup.html', {'message': message})