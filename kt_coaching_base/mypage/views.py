from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Sum
from rpg.models import Persona, Message
from account.models import Account
from community.models import Survey, Rating

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

# def myp_survey(request):
#     return render(request, 'mypage/myp_survey.html')

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

# @login_required
# def share_persona(request, persona_id):
#     try:
#         persona = Persona.objects.get(pk=persona_id, nickname=request.user)
#         persona.shared = True
#         persona.save()
#     except Persona.DoesNotExist:
#         return redirect('mypage:myp_survey')

#     return redirect('mypage:myp_survey')

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
    
def rating_list(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)
    ratings = Rating.objects.filter(survey__persona_id=persona)

    total_scores = {
        'score_1_total': ratings.aggregate(total=Sum('score_1'))['total'],
        'score_2_total': ratings.aggregate(total=Sum('score_2'))['total'],
        'score_3_total': ratings.aggregate(total=Sum('score_3'))['total'],
        'score_4_total': ratings.aggregate(total=Sum('score_4'))['total'],
        'score_5_total': ratings.aggregate(total=Sum('score_5'))['total'],
        'score_6_total': ratings.aggregate(total=Sum('score_6'))['total'],
        'score_7_total': ratings.aggregate(total=Sum('score_7'))['total'],
        'score_8_total': ratings.aggregate(total=Sum('score_8'))['total'],
        'score_9_total': ratings.aggregate(total=Sum('score_9'))['total'],
        'score_10_total': ratings.aggregate(total=Sum('score_10'))['total'],
        'score_11_total': ratings.aggregate(total=Sum('score_11'))['total'],
        'score_12_total': ratings.aggregate(total=Sum('score_12'))['total'],
        'score_13_total': ratings.aggregate(total=Sum('score_13'))['total'],
        'score_14_total': ratings.aggregate(total=Sum('score_14'))['total'],
    }

    context = {
        'persona': persona,
        'ratings': ratings,
        'total_scores': total_scores,
    }

    return render(request, 'mypage/rating_list.html', context)