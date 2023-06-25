from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rpg.models import Message
from account.models import Account
import numpy as np
import pandas as pd
import os

def result (request):
    if request.method == "POST":
        print("abc")
    else :
        return render(request, "analysis/result.html")
# Create your views here.

def intro (request):
    df = pd.DataFrame()
    p_id = request.session.get("persona_id")[0]["id"]
    questions = Message.objects.filter(persona=p_id, name=request.user.nickname)
    questions_list = [
        {
            'id': msg.id, 
            'name': msg.name, 
            'persona': msg.persona.id,  # assuming persona object has an id
            'content': msg.content, 
            'send_date': msg.send_date.isoformat(), 
            'voice_url': msg.voice_url,
            'csv_url': msg.csv_url
        } 
        for msg in questions
    ]
    
    for question in questions_list:
        csv_url = question['csv_url']

        # csv_url에서 CSV 파일을 읽어옴
        df_temp = pd.read_csv(csv_url)
        # 읽어온 DataFrame을 df 아래에 붙임
        df = pd.concat([df, df_temp], ignore_index=True)
    
    request.session["관점변화"] = 0
    request.session["부정"] = 0
    request.session["인정"] = 0
    request.session["존중"] = 0
    request.session["판단"] = 0
    
    l = len(df['predict'])
    if l > 0: 
        for i in range(l):
            request.session[df['predict'][i]] += 1
            print( df['predict'][i])
    else : # 아무 대화도 안한 경우 돌려보내기
        return redirect('rpg:rpg_start')
        
    perspective     = round((request.session.get("관점변화")/l) * 100, 0)
    negation        = round((request.session.get("부정")/l) * 100, 0)
    recognition     = round((request.session.get("인정")/l) * 100, 0)
    respect         = round((request.session.get("존중")/l) * 100, 0)
    judgment        = round((request.session.get("판단")/l) * 100, 0)
    pie_chart =   {
        "Perspective": perspective,
        "Negation": negation,
        "Recognition": recognition,
        "Respect": respect,
        "Feedback": judgment,
        "f_score" : request.session["scores"][-1],
        "socre_mem" : request.session.get("scores")
    }
    
    return render(request, "analysis/intro.html", pie_chart)