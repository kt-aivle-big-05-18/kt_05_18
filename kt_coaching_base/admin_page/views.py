from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from rpg.models import Persona
from account.models import Account, admin_info
import numpy as np
import pandas as pd
import os
import json

def admin_page (request):
    # Rank 종류별 갯수
    rank_counts = list(Persona.objects.values('rank').annotate(rank_count=Count('rank')))

    # Department 종류별 갯수
    department_counts = list(Persona.objects.values('department').annotate(department_count=Count('department')))

    # 성별 종류별 갯수
    gender_counts = Persona.objects.values('gender').annotate(gender_count=Count('gender'))

    # 상황 종류별 갯수
    topic_label_counts = list(Persona.objects.values('topic_label').annotate(topic_label_count=Count('topic_label')))

    # 성별 종류별 갯수
    career_counts = Persona.objects.values('career').annotate(career_count=Count('career'))

    # 상황 종류별 갯수
    age_counts = list(Persona.objects.values('age').annotate(age_count=Count('age')))

    # Total counts
    total_ranks = sum([item['rank_count'] for item in rank_counts])
    

    # Calculate ratios
    for item in rank_counts:
        item['rank_ratio'] = item['rank_count'] / total_ranks * 100

    for item in department_counts:
        item['department_ratio'] = item['department_count'] / total_ranks * 100
    
    for item in gender_counts:
        item['gender_ratio'] = item['gender_count'] / total_ranks * 100
    
    for item in topic_label_counts:
        item['topic_label_ratio'] = item['topic_label_count'] / total_ranks * 100

    for item in career_counts:
        item['career_ratio'] = item['career_count'] / total_ranks * 100
    
    for item in age_counts:
        item['age_ratio'] = item['age_count'] / total_ranks * 100
    
    context = {
        'rank_counts': json.dumps(list(rank_counts)),
        'department_counts': json.dumps(list(department_counts)),
        'gender_counts': json.dumps(list(gender_counts)),
        'topic_label_counts': json.dumps(list(topic_label_counts)),
        'career_counts': json.dumps(list(career_counts)),
        'age_counts': json.dumps(list(age_counts)),
    }

    return render(request, "admin_page/admin_page.html", context)
