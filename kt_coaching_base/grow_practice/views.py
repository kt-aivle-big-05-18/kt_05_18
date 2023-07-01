from django.shortcuts import render
# rpg/views.py

# 일반 파이썬 패키지
import numpy as np
import pandas as pd
import os
import pickle

# Django
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
import openai, json, requests
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def grow_practice(request):
    return render(request, 'grow_practice/grow_practice.html')

#----------------------------------------------------------------------------------------------------#
# GROW 연습 메인
#----------------------------------------------------------------------------------------------------#
openai.api_key = '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'

def grow(request):
    # HTTP 요청이 POST 방식일 경우
    if request.method == "POST":
        message = request.POST.get("message") # 사용자가 입력한 한국어 메세지
        print(message)
        
        # 번역된 사용자 입력 메세지를 messages에 추가
        # request.session.get('messages').append({"role": "user", "content": message})
        
        # OpenAI의 챗봇 API에 메시지 리스트를 전달하고 응답을 받아오기
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= [{"role": "user", "content": message}]
        )
        print(response.choices[0].message.content)
        print(response)
        # trans_ = retranslate(response.choices[0].message.content) # 한국어 번역한 chatgpt 답변 메세지
        # request.session.get('messages').append({"role": "assistant", "content": response.choices[0].message.content})
        data = { # json형식으로 respone 해줄 데이터
            'message' : response.choices[0].message.content
        }
        return JsonResponse(data)
    
    else :
        return render(request, "grow_practice/grow_practice.html")
