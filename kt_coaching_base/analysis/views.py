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
        return render(request, "analysis/analysis.html")
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
        
    l = len(df['predict'])
    for i in range(l):
        print(df['predict'][i])
    return render(request, "analysis/intro.html")