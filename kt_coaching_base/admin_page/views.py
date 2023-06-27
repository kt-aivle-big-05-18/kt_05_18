from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Case, When, Value, CharField
from rpg.models import Persona
from account.models import Account, admin_info
import numpy as np
import pandas as pd
import os
import json

def admin_persona(request):
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
    age_counts = (
        Persona.objects
        .annotate(age_group=Case(
            When(age__range=(20, 29), then=Value('20대')),
            When(age__range=(30, 39), then=Value('30대')),
            When(age__range=(40, 49), then=Value('40대')),
            When(age__range=(50, 59), then=Value('50대')),
            When(age__range=(60, 69), then=Value('60대')),
            # 추가적인 연령대 범위를 필요에 따라 추가해주세요
            default=Value('기타'),
            output_field=CharField(),
        ))
        .values('age_group')
        .annotate(age_group_count=Count('age_group'))
    )

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
        item['age_group_ratio'] = item['age_group_count'] / total_ranks * 100

    context = {
        'rank_counts': json.dumps(list(rank_counts)),
        'department_counts': json.dumps(list(department_counts)),
        'gender_counts': json.dumps(list(gender_counts)),
        'topic_label_counts': json.dumps(list(topic_label_counts)),
        'career_counts': json.dumps(list(career_counts)),
        'age_counts': json.dumps(list(age_counts)),
    }

    return render(request, "admin_page/admin_persona.html", context)


def admin_page(request):
    return render(request, "admin_page/admin_page.html")