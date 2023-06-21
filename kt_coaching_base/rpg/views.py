# rpg/views.py

# 일반 파이썬 패키지
import numpy as np
import pandas as pd
import os

# Django
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
import openai, json, requests
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# DB 관련
from .forms import RegisterPersona
from .models import Persona, Message
from account.models import Account

# Goolge stt/tts
from google.cloud import speech, texttospeech
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account

# 인코딩 관련
import soundfile as sf
import scipy.io.wavfile as wav
from scipy.signal import resample
from scipy.io.wavfile import write
import wave
import base64
from io import BytesIO
import sounddevice as sd

# 전처리 및 AI 분류 관련
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sentence_transformers import SentenceTransformer
import librosa
import random
import re
#----------------------------------------------------------------------------------------------------------------------#
# 0. 필요 install 목록
# pip install soundfile
# pip install sounddevice
# pip install --upgrade google-api-python-client
# pip install google-cloud-speech
# pip install google-cloud-texttospeech
# pip install openai
# pip install sentence-transformers
# 구글 stt 관련 추가로 설정해야함.
#----------------------------------------------------------------------------------------------------------------------#

# request 매개변수를 갖는 함수는 rpg.js와 urls.py를 참고해서 이해하면 더 쉽습니다. -from 충영

#----------------------------------------------------------------------------------------------------------------------#
# 1. 네이버 번역 관련
#----------------------------------------------------------------------------------------------------------------------#

# OpenAI의 api_key를 설정합니다.
openai.api_key = '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'


def translate(text):
    # 네이버 클라우드 플랫폼에서 발급받은 ID와 Secret을 입력
    client_id = 'k932basti3'
    client_secret = 'PWJGrQ1Wa6sdkX1Dy69sideTenzGQGominAx3NMW'
    # 파파고 번역 API를 사용하기 위한 설정
    # 한국어(ko)를 영어(en)로 번역하도록 설정
    data = {'source':'ko', 'target':'en', 'text': text}
    url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
    
    # 네이버 API를 사용하기 위해 요청 헤더에 ID와 Secret을 추가
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret
    }
    
    # 파파고 API에 POST 요청을 보내고 응답을 받기
    response = requests.post(url, headers=headers, data=data)
    
    # 응답을 JSON 형식으로 파싱하고 번역된 텍스트를 반환
    res = json.loads(response.text)
    return res['message']['result']['translatedText']

def retranslate(text):
    # 네이버 클라우드 플랫폼에서 발급받은 ID와 Secret을 입력
    client_id = 'k932basti3'
    client_secret = 'PWJGrQ1Wa6sdkX1Dy69sideTenzGQGominAx3NMW'
    
    # 파파고 번역 API를 사용하기 위한 설정
    # 영어(en)를 한국어(ko)로 번역하도록 설정합니다. 공손한 어투를 사용하도록 설정
    data = {'source':'en', 'target':'ko', 'text': text, 'honorific':'true'}
    url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
    
    # 네이버 API를 사용하기 위해 요청 헤더에 ID와 Secret을 추가
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret
    }
    
    # 파파고 API에 POST 요청을 보내고 응답을 받기
    response = requests.post(url, headers=headers, data=data)
    
    # 응답을 JSON 형식으로 파싱하고 번역된 텍스트를 반환
    res = json.loads(response.text)
    return res['message']['result']['translatedText']

#----------------------------------------------------------------------------------------------------------------------#
# 2. 패르소나 생성
#----------------------------------------------------------------------------------------------------------------------#

def persona(request):
    # 로그인 안했으면 로그인 하러 가는걸로 ^^
    if not request.user.is_authenticated :
        return redirect('account:login')
    
    # POST라면 입력한 내용을 form을 이용하여 데이터베이스에 저장
    if request.method == "POST":
        form = RegisterPersona(request.POST)
        # 유효성 검사
        if form.is_valid():
            form.nickname = request.user.nickname
            persona = form.save(commit=False)
            persona.nickname = Account.objects.get(nickname=request.user.nickname)
            persona.save()
            request.session['visited_persona'] = True
            request.session.get("persona_set").append({
                                    "role" : "system", 
                                    "content" : translate( "다음 대화부터 assistant는 상사와 대화하는 {0}세인 {1} {2}{3}입니다.".format(
                                        form.cleaned_data['age'], # 0 나이 - gpt
                                        form.cleaned_data['gender'], # 1 성별 - gpt
                                        form.cleaned_data['department'], # 2 직군 - gpt
                                        form.cleaned_data['rank'],))  # 3 직급 - gpt
                                    })
            persona_id = Persona.objects.filter(nickname=request.user.nickname).last()
            request.session.get("persona_id").append({
                "id" : f"{persona_id.id}"
            })
            request.session["voice"] = request.POST.get('voice') # 챗봇의 목소리 형태를 저장할 세션 변수
            request.session["count"] = 0 # 대화 주고받는 순서 저장할 세션 변수
            # 이제 여기에 스케일러 fit 할 예정입니다!
            return redirect("rpg:rpg_start")
    else : # GET 방식인 경우
        # 폼 생성
        form = RegisterPersona(request.POST or None)
        # 페르소나 세션 생성
        request.session["persona_id"] = []
        request.session["persona_set"] = []
        return render(request, 'rpg/persona.html', {"form": form})

#----------------------------------------------------------------------------------------------------#
# 3. 롤플레잉 실행 과정 
#----------------------------------------------------------------------------------------------------#

def rpg(request):
    if len(request.session.get("persona_set")) == 0 :
        form = RegisterPersona(request.POST or None)
        return redirect("rpg:persona")
    
    base_dir = settings.BASE_DIR # 기본 디렉터리 경로 불러오기
    p_id = request.session.get("persona_id")[0]["id"] # 채팅방 id 불러오기
    print(p_id)
    
    # HTTP 요청이 POST 방식일 경우
    if request.method == "POST":
        message = request.POST.get("message") # 사용자가 입력한 한국어 메세지
        
        # 번역된 사용자 입력 메세지를 messages에 추가
        request.session.get('messages').append({"role": "user", "content": translate(message)})
        count = request.session.get("count") # url 경로 저장을 위한 대화 카운트 설정
        user_voice_url = os.path.join(base_dir, 'rpg/static/voice/{0}_{1}.wav'.format(p_id, count))
        
        # ---------------------- AI 전처리 / AI prediction -----------------------#
        m_df = classification_model(message, user_voice_url)
        m_df_url = os.path.join(base_dir, 'rpg/static/df_csv/{0}_{1}.csv'.format(p_id, count))
        m_df.to_csv(m_df_url, index=False)
        # ------------------------------------------------------------------------#
        
        # 유저 메세지내용, 음성녹음 내용을 테이블에 저장
        user_message_obj = Message(
            name = request.user.nickname,
            persona = Persona.objects.get(id=int(p_id)),
            content = request.POST.get("message"),
            voice_url = user_voice_url,
            csv_url = m_df_url
        )
        user_message_obj.save()
        
        request.session["count"] += 1
        count = request.session.get("count")
        
        # OpenAI의 챗봇 API에 메시지 리스트를 전달하고 응답을 받아오기
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=request.session.get('messages')
        )
        
        # 번역된 챗봇의 메시지를 메시지 리스트에 추가
        request.session.get('messages').append({"role": "assistant", "content": response.choices[0].message.content})
        trans_ = retranslate(response.choices[0].message.content) # 한국어 번역한 chatgpt 답변 메세지
        
        voice_select = request.session.get('voice')  # 선택한 음성 옵션 가져오기
        if voice_select=='ko-KR-Neural2-A' or voice_select=='ko-KR-Neural2-B' or voice_select=='ko-KR-Wavenet-B':
            gender_select = 'FEMALE'
            generate_speech(trans_, voice_select, gender_select, p_id , count)  # 음성 파일 생성 함수 호출
            
        elif voice_select == 'ko-KR-Standard-D' or voice_select=='ko-KR-Wavenet-C' or voice_select=='ko-KR-Standard-C':
            gender_select = 'MALE'
            generate_speech(trans_, voice_select, gender_select, p_id, count)  # 음성 파일 생성 함수 호출
        
        # 답장 온거 저장된 wav파일 경로
        path_gpt_voice = os.path.join(base_dir, 'rpg/static/voice/{0}_{1}.wav'.format(p_id, count))
        
        # gpt 답장 메세지 DB 전송
        gpt_response_obj = Message(
            name="gpt",
            persona = Persona.objects.get(id=int(p_id)),
            content = trans_,
            voice_url = path_gpt_voice
        )
        gpt_response_obj.save()
        
        # 음성 파일의 경로를 반환하는 HttpResponse 객체 생성
        with open(path_gpt_voice, 'rb') as voice_file:
            encoded_voice = base64.b64encode(voice_file.read()).decode('utf-8')

        data = { # json형식으로 respone 해줄 데이터
            'message' : trans_,
            'voice': encoded_voice,
            'path': "{0}_{1}.wav".format(p_id, count)
        }
        request.session["count"] += 1 # 음성녹음 이름을 조합을 위한 count + 1
        return JsonResponse(data)
    else :
        request.session['messages'] = request.session.get("persona_set") # 초기 패르소나 설정을 메세지에 추가하기
        return render(request, "rpg/rpg.html")

#----------------------------------------------------------------------------#
# 4. tts
#----------------------------------------------------------------------------#

def generate_speech(text, voice, gender, p_id, count):
    # 클라이언트 인스턴스화
    client = texttospeech.TextToSpeechClient()

    # 합성할 텍스트 입력 설정
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    # 선택한 음성 옵션 설정
    voice = texttospeech.VoiceSelectionParams(
        language_code='ko-KR',
        name=voice,
        ssml_gender=gender,
    )
    
    audio_config = texttospeech.AudioConfig(
        # pitch=10,
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )
    
    # 텍스트를 음성으로 변환하는 요청 생성
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    # 응답의 오디오 컨텐츠는 이진 데이터입니다.
    with open('rpg/static/voice/{0}_{1}.wav'.format(p_id, count), 'wb') as out:
        # 응답을 출력 파일에 작성합니다.
        out.write(response.audio_content)

#---------------------------------------------------------------------------#
# 5. stt
#---------------------------------------------------------------------------#

def stt(request):
        p_id = request.session.get("persona_id")[0]["id"]
        count = request.session.get("count")

        audio_data = request.FILES['audio_data']

        fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, '/rpg/static/voice'))
        filename = fs.save('{0}_{1}.wav'.format(p_id, count), audio_data)
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
        language_code="ko-KR",
    )
    response = client.recognize(config=config, audio=audio)

    # 변환된 텍스트 추출
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "

    return transcript

#---------------------------------------------------------------------------#
# 6. AI
#---------------------------------------------------------------------------#

#-------- 전처리 함수 정의 ----------#
def noise(data):
    noise_amp = 0.035*np.random.uniform()*np.amax(data)
    data = data + noise_amp*np.random.normal(size=data.shape[0])
    return data

def extract_features(data, sample_rate):
    # ZCR
    result = np.array([])
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
    result=np.hstack((result, zcr)) # stacking horizontally

    # Chroma_stft
    stft = np.abs(librosa.stft(data))
    chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    result = np.hstack((result, chroma_stft)) # stacking horizontally

    # MFCC
    mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mfcc)) # stacking horizontally

    # Root Mean Square Value
    rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
    result = np.hstack((result, rms)) # stacking horizontally

    # MelSpectogram
    mel = np.mean(librosa.feature.melspectrogram(y=data, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mel)) # stacking horizontally

    return result

def get_features(path):

    data, sample_rate = librosa.load(path, duration=2.5, offset=0.0)

    # without augmentation
    res1 = extract_features(data, sample_rate)
    result = np.array(res1)

    # data with noise
    noise_data = noise(data)
    res2 = extract_features(noise_data, sample_rate)
    result = np.concatenate((result, res2), axis = 0)

    return result

class text_embedding():
  def __init__(self, model_name):
    self.model_name = model_name

  def fit(self, new_sent, y=None):
        return self

  def transform(self, new_sent):
        embedding_model = SentenceTransformer(self.model_name)
        embedding_vec = embedding_model.encode(new_sent['sentence'])
        X_val = np.concatenate((new_sent.drop(['sentence'], axis = 1), embedding_vec), axis = 1)
        return X_val

## 문단 > 문장 단위로 나누기
def split_into_sentences(paragraph):
    sentences = re.split("(?<=[.!?])\s+", paragraph)
    return sentences


#---------------- 모델 불러와서 분류하기 -------------#

def classification_model(new_sentence, new_voice):
  output_dic = {0:'관점변화', 1:'부정', 2:'인정', 3:'존중', 4:'피드백'}
  final_result = pd.DataFrame()
  new_sents = pd.DataFrame(split_into_sentences(new_sentence))

  # wav 파일 불러오기
  model_path = os.path.join(settings.BASE_DIR, 'rpg/analysis_model/')
  new_wav = new_voice # wav 파일 경로

  # 데이터 전처리 함수 불러오기
  scaler = StandardScaler()
  txt_embed = text_embedding(model_name = 'jhgan/ko-sroberta-multitask')

  if os.path.isfile(new_wav) and len(new_sents)<3:  # wav파일 있고 2문장 이하면 voice+text 사용
    print('VOICE', len(new_sents))
    new_sent = pd.DataFrame([new_sentence])
    new_sent.columns = ['sentence']
    # extract voice feature vector
    new_voice = pd.DataFrame(get_features(new_wav)).transpose()
    new_df = pd.concat([new_voice, new_sent], axis=1)

    # read voice training data
    voice_df = pd.read_csv(os.path.join(model_path, '230621_voice_df.csv'))

    # 새로운 데이터 전처리
    X_test = txt_embed.transform(new_df) # extract text embedding vector

    scaler.fit_transform(voice_df)
    x_test = scaler.transform(X_test)
#-----------------------------------------------------------------------#
    # 긍정 부정 분류 모델 불러옴, 긍부정 예측
   
    model1 = load_model(os.path.join(model_path, '230621_voice_model1.h5'))
    y_pred1 = model1.predict(x_test, verbose=0).round()

    pred1_df = pd.DataFrame(x_test)
    pred1_df['predict1'] = y_pred1

    pred_neg = pred1_df.loc[pred1_df['predict1'] == 1]
    pred_neg['predict'] = '부정'

    pred_pos = pred1_df.loc[pred1_df['predict1'] == 0]
    x_test2 = pred_pos.drop('predict1', axis=1)

    if len(x_test2) > 0:
      if os.path.isfile(new_wav): # wav 파일 있으면 voice feature 제거하고 text로만 2차분류함
          voice_cols = [x for x in range(324)]
          x_test2 = pd.DataFrame(x_test2).drop(voice_cols, axis=1) # delete voice feature vector

      # 2차 분류 모델 불러옴, 최종 분류
      model2 = load_model(os.path.join(model_path, '230621_result_model2.h5'))
      y_fin = np.argmax(model2.predict(x_test2, verbose=0), axis=1)

      pred_pos['predict'] = np.vectorize(output_dic.get)(y_fin)

    final_result['sentence'] = new_sent['sentence']
    final_result['predict'] = pd.concat([pred_neg, pred_pos]).sort_index()['predict']

  else: # wav 없거나 3문장 이상이면 text만 사용
    new_sents.columns = ['sentence']
    
    text_df = pd.read_csv(os.path.join(model_path, '230621_text_df.csv'))

    # 새로운 데이터 전처리
    X_test = txt_embed.transform(new_sents) # extract text embedding vector

    scaler.fit_transform(text_df)
    x_test = scaler.transform(X_test)

    # 긍정 부정 분류 모델 불러옴, 긍부정 예측
    
    model1 = load_model(os.path.join(model_path, '230621_text_model1.h5'))
    y_pred1 = model1.predict(x_test, verbose=0).round()

    pred1_df = pd.DataFrame(x_test)
    pred1_df['predict1'] = y_pred1

    pred_neg = pred1_df.loc[pred1_df['predict1'] == 1]
    pred_neg['predict'] = '부정'

    pred_pos = pred1_df.loc[pred1_df['predict1'] == 0]
    x_test2 = pred_pos.drop('predict1', axis=1)

    if len(x_test2) > 0:
      # 2차 분류 모델 불러옴, 최종 분류
      model2 = load_model(os.path.join(model_path, '230621_result_model2.h5'))
      y_fin = np.argmax(model2.predict(x_test2, verbose=0), axis=1)

      pred_pos['predict'] = np.vectorize(output_dic.get)(y_fin)

    final_result['sentence'] = new_sents['sentence']
    final_result['predict'] = pd.concat([pred_neg, pred_pos]).sort_index()['predict']

  return final_result