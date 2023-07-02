from django.shortcuts import render
# rpg/views.py

# 일반 파이썬 패키지
import numpy as np
import pandas as pd
import os
import pickle
import random

# Django
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
import openai, json, requests
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Goolge stt/tts
from google.cloud import speech, texttospeech
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account

# 인코딩 관련
import scipy.io.wavfile as wav
from scipy.signal import resample
from scipy.io.wavfile import write
import wave
import base64
from io import BytesIO
import subprocess

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

def stt(request):
    p_id = request.session.get("persona_id")[0]["id"]
    count = request.session.get("count")

    audio_data = request.FILES['audio_data']

    fs = OverwriteStorage(location=os.path.join(settings.BASE_DIR, 'rpg/static/voice'))
    filename = fs.save('{0}_{1}.webm'.format(p_id, count), audio_data)
    uploaded_file_url = fs.path(filename)

    trans_voice_message = transcribe_audio(uploaded_file_url)

    return JsonResponse({"text" : trans_voice_message})


#---------------------------------------------------------------------------#
# stt
#---------------------------------------------------------------------------#

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(self.location, name))
        return name

def stt(request):
    audio_data = request.FILES['audio_data']

    fs = OverwriteStorage(location=os.path.join(settings.BASE_DIR, 'grow_practice/static/voice'))
    letters = "abcdefghijklmnopqrstuvwxyz0123456789"
    filename = ''.join(random.choice(letters) for _ in range(20))+'.webm'

    filename = fs.save(filename, audio_data)
    uploaded_file_url = fs.path(filename)

    trans_voice_message = transcribe_audio(uploaded_file_url)

    return JsonResponse({"text" : trans_voice_message})

def transcribe_audio(file_path):
    
    # Speech-to-Text 클라이언트 생성
    client = speech.SpeechClient()

    # 녹음 파일 읽기
    with open(file_path, 'rb') as audio_file:
        audio_data = audio_file.read()

    # 음성 데이터 인식 요청 생성
    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        # sample_rate_hertz=44100,
        language_code="ko-KR",
    )
    response = client.recognize(config=config, audio=audio)

    # 변환된 텍스트 추출
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "

    return transcript